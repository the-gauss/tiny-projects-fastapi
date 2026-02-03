from __future__ import annotations

"""
FastAPI application.

This app supports:
- `POST /upload`: upload a file + caption, stored in Postgres (BYTEA) for local testing.
- `GET /feed`: list posts newest-first.
- `GET /media/{post_id}`: serve stored bytes for posts uploaded via `/upload`.
"""

from contextlib import asynccontextmanager
import uuid

from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile  # pyright: ignore[reportMissingImports]
from fastapi.responses import Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import Post, create_db_and_tables, get_async_session
from app.schemas import FeedResponse, PostResponse

@asynccontextmanager    # Converts the function into a context manager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    # Everything before yield runs exactly once, right when the server starts up, but before it begins listening for HTTP requests.
    yield   # This is the moment where the application lives
    # Everything after yield runs exactly once, right when the server is shutting down.

app = FastAPI(lifespan=lifespan)

# @app.get('/posts')      # a get request for /posts endpoint
# def get_all_posts(limit: int = 10):    # this function is triggered when the endpoint is accessed
#     if limit:
#         return list(text_posts.values())[:limit]
#     return text_posts   # Return either a Pydantic Object or a Dictionary

# @app.get('/posts/{id}')    # a request with a path parameter - path params (/) go in decorator args, query params (?) go in function args
# def get_post(id: int):
#     if id not in text_posts:
#         raise HTTPException(status_code=404, detail="Post not found!")  # raise the HTTPException, we can't use try-except here cuz we need to RAISE this error, not catch any.
#     else:
#         return text_posts.get(id)
    
# @app.post("/posts")
# def create_post(post: CreatePost) -> PostResponse:  # post takes a Pydantic schema that it'll follow
#     new_post = {'title': post.title, 'content': post.content}
#     text_posts[max(text_posts.keys())+1] = new_post
#     return new_post

@app.post("/upload", response_model=PostResponse)
async def upload_file(
    file: UploadFile = File(...),   # File() tells FastAPI to expect a file upload
    caption: str = Form(''),    # Form tells it to extract non-file form fields like text inputs etc.
    session: AsyncSession = Depends(get_async_session)  # Depends is used to inject dependencies like databases etc. A dependency is an external function/class that the route depends on like DB sesssions, authentication, settings.
):  # arguments of a post function form the request body; arguments of a get function form the query parameters
    # NOTE: `UploadFile` streams uploads efficiently. We still read into memory here
    # because we're persisting into Postgres BYTEA for local/dev testing.
    # For large uploads in production, stream to object storage instead.
    post_id = uuid.uuid4()
    media_url = f"/media/{post_id}"

    try:
        media_bytes = await file.read()
        if not media_bytes:
            raise HTTPException(status_code=400, detail="Empty upload.")

        post = Post(
            id=post_id,
            caption=caption,
            url=media_url,
            file_type=file.content_type or "application/octet-stream",
            file_name=file.filename or f"{post_id}",
            media_bytes=media_bytes,
        )

        session.add(post)  # Stage changes
        await session.commit()
        await session.refresh(post)  # Hydrate server-side defaults (e.g. created_at)
        return PostResponse.model_validate(post)
    except HTTPException:
        # Preserve intentionally raised HTTP errors (e.g. validation failures).
        await session.rollback()
        raise
    except Exception:
        # Ensure we don't leak a failed transaction to later requests.
        await session.rollback()
        raise HTTPException(status_code=500, detail="Upload failed.")
    finally:
        # FastAPI will close the underlying file after the request, but closing early
        # is safe and avoids holding file handles longer than necessary.
        await file.close()


@app.get("/media/{post_id}")
async def get_media(
    post_id: uuid.UUID,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Serve stored media bytes for an uploaded post.

    We return a raw `Response` so clients can render the media directly.
    """
    result = await session.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post or not post.media_bytes:
        raise HTTPException(status_code=404, detail="Media not found.")

    return Response(
        content=post.media_bytes,
        media_type=post.file_type,
        headers={"Content-Disposition": f'inline; filename="{post.file_name}"'},
    )

@app.get("/feed", response_model=FeedResponse)
async def get_feed(
    session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = result.scalars().all()
    return FeedResponse(posts=[PostResponse.model_validate(p) for p in posts])
