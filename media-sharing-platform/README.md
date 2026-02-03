# Media Sharing Platform

A FastAPI-based media sharing platform backed by Postgres.

## 🚀 Features

- Upload and share images with captions
- Feed view with chronologically ordered posts
- Media stored in Postgres (BYTEA) for local/dev testing
- Async SQLAlchemy + Postgres
- FastAPI backend with Pydantic validation

## 📋 Prerequisites

- Python 3.9+
- [uv](https://github.com/astral-sh/uv) package manager
- Local Postgres running

## 🛠️ Setup

### 1. Install Dependencies

```bash
uv sync
```

### 2. Configure Environment Variables

The `.env` file should already be configured with:
- `DATABASE_URL`: Postgres async SQLAlchemy URL (example below)

Example:

```bash
DATABASE_URL=postgresql+asyncpg://thory:0301sonaL@localhost:5432/media_sharing_platform
```

If your local Postgres is configured for peer auth (common for Homebrew installs), a socket URL can be simpler:

```bash
DATABASE_URL=postgresql+asyncpg:///media_sharing_platform
```

### 3. Initialize Database

Run the initialization script to create tables and seed with sample data:

```bash
uv run python init_db.py
```

This will:
- Create the database tables
- Seed the database with 5 sample posts

## 🎯 Running the Application

Start the development server:

```bash
uv run python main.py
```

Or using uvicorn directly:

```bash
uv run uvicorn app.app:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## 📡 API Endpoints

### Upload a Post
```
POST /upload
Content-Type: multipart/form-data

Parameters:
- file: The image file to upload
- caption: Optional caption for the post
```

### Get Feed
```
GET /feed

Returns a list of all posts ordered by creation date (newest first)
```

### Get Media
```
GET /media/{post_id}

Returns the raw bytes for media uploaded via `/upload`.
```

## 🗂️ Project Structure

```
media-sharing-platform/
├── app/
│   ├── __init__.py
│   ├── app.py          # FastAPI application and routes
│   ├── db.py           # Database models and configuration
│   ├── images.py       # ImageKit integration
│   └── schemas.py      # Pydantic schemas
├── main.py             # Application entry point
├── init_db.py          # Database initialization script
├── pyproject.toml      # Project dependencies
└── .env                # Environment variables
```

## 🧪 Development

The application uses:
- **FastAPI** for the web framework
- **SQLAlchemy** with async support for database ORM
- **asyncpg** for async Postgres connectivity
- **Pydantic** for data validation

## 📝 Notes

- Sample posts use Unsplash URLs for demonstration
- The application uses async/await for all database operations
- Uploaded media is stored in Postgres for local/dev testing
