"""
Database models + session management.

We use SQLAlchemy's async engine + `async_sessionmaker` so FastAPI handlers can
work with Postgres efficiently without blocking the event loop.
"""

from collections.abc import AsyncGenerator
import os
import uuid

from dotenv import load_dotenv
from sqlalchemy import Column, DateTime, ForeignKey, LargeBinary, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, relationship
from fastapi_users.db import SQLAlchemyUserDatabase, SQLAlchemyBaseUserTableUUID
from fastapi import Depends

load_dotenv()  # Load `.env` for local dev; in production, prefer real env vars.

# SQLAlchemy async URLs for Postgres look like:
#   postgresql+asyncpg://USER:PASSWORD@HOST:PORT/DBNAME
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not set. Add it to `media-sharing-platform/.env` "
        "(example: postgresql+asyncpg://thory:...@localhost:5432/media_sharing_platform)."
    )

class Base(DeclarativeBase):
    pass

class User(SQLAlchemyBaseUserTableUUID, Base):
    posts = relationship("Post", back_populates="user")

class Post(Base):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    caption = Column(Text)
    url = Column(String, nullable=False)  # Public URL the client can render (may be internal route)
    file_type = Column(String, nullable=False)  # MIME type (e.g. image/jpeg)
    file_name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="posts")

    # Store uploaded bytes in Postgres (BYTEA) for local/dev testing.
    # In production, prefer object storage (S3/GCS/etc.) and store only metadata + URL.
    media_bytes = Column(LargeBinary, nullable=True)


# `pool_pre_ping` keeps long-lived dev servers resilient to Postgres restarts.
engine = create_async_engine(DATABASE_URL, pool_pre_ping=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def create_db_and_tables():
    """Create tables for local/dev environments (no migrations required)."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Get a session that allows us to access the database engine and write and read asynchronously
async def get_async_session() -> AsyncGenerator[AsyncSession, None]: 
    async with async_session_maker() as session:
        yield session

async def get_user_db(AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)