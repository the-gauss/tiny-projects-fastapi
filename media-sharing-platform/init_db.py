"""
Database initialization and seeding script for the media sharing platform.
Run this script to create the database tables and populate with sample data.
"""
import asyncio
from app.db import create_db_and_tables, async_session_maker, Post
from datetime import datetime, timedelta


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
    print("🔧 Creating database tables...")
    await create_db_and_tables()
    print("✅ Database tables created successfully!")
    
    print("\n🌱 Seeding database with sample data...")
    await seed_database()
    print("\n✨ Database initialization complete!")


if __name__ == "__main__":
    asyncio.run(main())
