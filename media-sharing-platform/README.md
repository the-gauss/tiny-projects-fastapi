# Media Sharing Platform

A FastAPI-based media sharing platform with ImageKit integration for image hosting.

## 🚀 Features

- Upload and share images with captions
- Feed view with chronologically ordered posts
- ImageKit integration for image storage
- Async SQLite database
- FastAPI backend with Pydantic validation

## 📋 Prerequisites

- Python 3.9+
- [uv](https://github.com/astral-sh/uv) package manager
- ImageKit account (for image hosting)

## 🛠️ Setup

### 1. Install Dependencies

```bash
uv sync
```

### 2. Configure Environment Variables

The `.env` file should already be configured with:
- `DATABASE_URL`: SQLite database path
- `IMAGEKIT_PRIVATE_KEY`: Your ImageKit private key
- `IMAGEKIT_PUBLIC_KEY`: Your ImageKit public key
- `IMAGEKIT_URL`: Your ImageKit URL endpoint

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
- **aiosqlite** for async SQLite operations
- **ImageKit** for image hosting and management
- **Pydantic** for data validation

## 📝 Notes

- The database file `test.db` will be created automatically
- Sample posts use Unsplash URLs for demonstration
- The application uses async/await for all database operations
- ImageKit credentials must be valid for actual image uploads to work
