"""
Pydantic schemas for request/response models.

We use `from_attributes=True` to allow `model_validate()` directly from SQLAlchemy
ORM instances without manually building dicts.
"""

from __future__ import annotations

from datetime import datetime
import uuid

from pydantic import BaseModel, ConfigDict


class PostResponse(BaseModel):
    """Public representation of a post returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    caption: str | None = None
    url: str
    file_type: str
    file_name: str
    created_at: datetime


class FeedResponse(BaseModel):
    """Feed payload returned by `GET /feed`."""

    posts: list[PostResponse]
