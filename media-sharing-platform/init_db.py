"""
Database initialization and seeding script for the media sharing platform.
Run this script to create the database tables and populate with sample data.
"""
import asyncio
import re

import asyncpg
from sqlalchemy.engine.url import make_url

from app.db import DATABASE_URL, Post, async_session_maker, create_db_and_tables
from datetime import datetime, timedelta


async def ensure_database_exists() -> None:
    """
    Ensure the target Postgres database exists.

    SQLAlchemy cannot connect to a database that doesn't exist yet, so for local/dev
    we connect to the default `postgres` database using `asyncpg` and create the
    target database when missing.
    """
    url = make_url(DATABASE_URL)
    db_name = url.database
    if not db_name:
        raise RuntimeError("DATABASE_URL is missing a database name.")

    # Avoid SQL injection when using the database name as an identifier.
    if not re.fullmatch(r"[A-Za-z0-9_]+", db_name):
        raise RuntimeError(
            f"Refusing to create database with unexpected name: {db_name!r}. "
            "Use only letters, digits, and underscore."
        )

    admin_url = url.set(database="postgres")
    # asyncpg expects `postgresql://...`, not SQLAlchemy's `postgresql+asyncpg://...`.
    admin_dsn = str(admin_url).replace("postgresql+asyncpg://", "postgresql://", 1)

    try:
        conn = await asyncpg.connect(admin_dsn)
    except asyncpg.InvalidPasswordError as exc:
        raise RuntimeError(
            "Postgres authentication failed for the configured DATABASE_URL.\n"
            "If you're using a local Homebrew Postgres with peer auth, try a socket URL:\n"
            "  DATABASE_URL=postgresql+asyncpg:///media_sharing_platform\n"
            "Otherwise, set/reset the password for the role and retry.\n"
            "Example:\n"
            "  psql postgres\n"
            "  ALTER USER thory WITH PASSWORD '0301sonaL';\n"
            "  CREATE DATABASE media_sharing_platform OWNER thory;"
        ) from exc
    try:
        exists = await conn.fetchval(
            "SELECT 1 FROM pg_database WHERE datname = $1",
            db_name,
        )
        if not exists:
            await conn.execute(f'CREATE DATABASE "{db_name}"')
            print(f"✅ Created database: {db_name}")
    finally:
        await conn.close()


async def seed_database():
    """Seed the database with sample posts."""
    async with async_session_maker() as session:
        # Sample posts data
        sample_posts = [
            {
                "caption": "Beautiful sunset at the beach 🌅",
                "url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e",
                "file_type": "photo",
                "file_name": "sunset_beach.jpg"
            },
            {
                "caption": "Mountain adventure 🏔️",
                "url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4",
                "file_type": "photo",
                "file_name": "mountain_view.jpg"
            },
            {
                "caption": "Urban exploration 🏙️",
                "url": "https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b",
                "file_type": "photo",
                "file_name": "city_skyline.jpg"
            },
            {
                "caption": "Nature walk in the forest 🌲",
                "url": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e",
                "file_type": "photo",
                "file_name": "forest_path.jpg"
            },
            {
                "caption": "Coffee time ☕",
                "url": "https://images.unsplash.com/photo-1511920170033-f8396924c348",
                "file_type": "photo",
                "file_name": "coffee_art.jpg"
            }
        ]
        
        # Create posts with different timestamps
        for i, post_data in enumerate(sample_posts):
            post = Post(
                caption=post_data["caption"],
                url=post_data["url"],
                file_type=post_data["file_type"],
                file_name=post_data["file_name"],
                created_at=datetime.utcnow() - timedelta(hours=len(sample_posts) - i)
            )
            session.add(post)
        
        await session.commit()
        print(f"✅ Successfully seeded database with {len(sample_posts)} sample posts!")


async def main():
    """Initialize database and optionally seed it."""
    print("🔧 Ensuring database exists...")
    await ensure_database_exists()

    print("🔧 Creating database tables...")
    await create_db_and_tables()
    print("✅ Database tables created successfully!")
    
    print("\n🌱 Seeding database with sample data...")
    await seed_database()
    print("\n✨ Database initialization complete!")


if __name__ == "__main__":
    asyncio.run(main())
