from fastapi import FastAPI, HTTPException # pyright: ignore[reportMissingImports]
from app.schemas import CreatePost, PostResponse

app = FastAPI()

# Pre-populated dummy posts
text_posts = {
    1: {"title": "Welcome to MediaShare", "content": "This is our first post. Enjoy exploring the platform!"},
    2: {"title": "Tips & Tricks", "content": "Use the search bar to quickly find your favorite content."},
    3: {"title": "Community Guidelines", "content": "Be respectful and keep conversations constructive and friendly."},
    4: {"title": "Feature Spotlight: Playlists", "content": "Group your favorite media into playlists to share with friends."},
    5: {"title": "Weekly Challenge", "content": "Post your best sunset photo this week and tag #SunsetVibes."},
    6: {"title": "Behind the Scenes", "content": "A peek at how we built our upload pipeline and CDN caching."},
    7: {"title": "Release Notes 0.1.0", "content": "Initial release with auth, posts, and basic search."},
    8: {"title": "Security Update", "content": "We’ve improved session management and password hashing."},
    9: {"title": "Creator Program", "content": "Apply to our creator program for early feature access."},
    10: {"title": "Your Feedback", "content": "Tell us what to build next—comments and upvotes now count!"},
}

@app.get('/posts')      # a get request for /posts endpoint
def get_all_posts(limit: int = 10):    # this function is triggered when the endpoint is accessed
    if limit:
        return list(text_posts.values())[:limit]
    return text_posts   # Return either a Pydantic Object or a Dictionary

@app.get('/posts/{id}')    # a request with a path parameter - path params (/) go in decorator args, query params (?) go in function args
def get_post(id: int):
    if id not in text_posts:
        raise HTTPException(status_code=404, detail="Post not found!")  # raise the HTTPException, we can't use try-except here cuz we need to RAISE this error, not catch any.
    else:
        return text_posts.get(id)
    
@app.post("/posts")
def create_post(post: CreatePost) -> PostResponse:  # post takes a Pydantic schema that it'll follow
    new_post = {'title': post.title, 'content': post.content}
    text_posts[max(text_posts.keys())+1] = new_post
    return new_post

# Solve first - new_post isn't a CreatePost type

