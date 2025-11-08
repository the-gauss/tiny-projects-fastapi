from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends # pyright: ignore[reportMissingImports]
from app.schemas import CreatePost, PostResponse
from app.db import Post, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select
from app.images import imagekit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
import shutil
import os
import uuid
import tempfile

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

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

@app.post('/upload')
async def upload_file(
    file: UploadFile = File(...),
    caption: str = Form(''),
    session: AsyncSession = Depends(get_async_session)
):  # arguments of a post function form the request body; arguments of a get function form the query parameters
    post = Post(
        caption = caption,
        url = 'dummy url',
        file_type = 'photo',
        file_name = 'dummy name'
    )
    session.add(post)       # like staging to add 
    await session.commit()  # actually add to the database
    await session.refresh(post) #hydrates the other auto fields (like id etc) we didn't provide
    return post     # return the post object (may be so that it can be used at the front)

@app.get('/feed')
async def get_feed(
    session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()]

    posts_data = []
    for post in posts:
        posts_data.append(
            {
                'id': str(post.id),
                'caption': post.caption,
                'url': post.url,
                'file_type': post.file_type,
                'file_name': post.file_name,
                'created_at': post.created_at.isoformat()
            }
        )

    return {'posts': posts_data}

