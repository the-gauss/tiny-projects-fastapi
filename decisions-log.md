# Decisions Log

This repo includes a FastAPI service under `media-sharing-platform/`. This log records decisions that materially affect architecture, local testability, and likely production direction.

## 2026-02-03 — Persistence: local Postgres via async SQLAlchemy

We standardize local development on Postgres using SQLAlchemy’s async engine (`postgresql+asyncpg`). This keeps the local environment closer to typical production deployments (concurrency characteristics, UUIDs, and binary columns) and avoids SQLite-specific behavior.

Operationally, local auth can vary (password vs peer/socket), so the project supports both styles via `DATABASE_URL` in `media-sharing-platform/.env`.

## 2026-02-03 — Media storage: store bytes in Postgres for dev/test

For the current functionality, uploaded media is stored directly in Postgres (`BYTEA`) alongside its metadata. The primary intent is end-to-end testability without external services; it is not a long-term scaling strategy for large media.

The API generates an internal URL for each upload and serves it back via the application so a client can render media immediately.

## 2026-02-03 — API: first-party media serving endpoint

We expose `GET /media/{post_id}` to return the raw stored bytes with the persisted MIME type. This removes third‑party hosting requirements and keeps the demo flow self-contained.

## 2026-02-03 — Schema management: `create_all()` for now

For fast iteration, schema creation uses `Base.metadata.create_all()` (via the FastAPI lifespan hook and `init_db.py`). Once the schema stabilizes, the expected upgrade path is Alembic migrations to support controlled rollouts.

## 2026-02-03 — Responses: typed Pydantic models validated from ORM objects

Responses use explicit FastAPI `response_model` types, and Pydantic is configured to validate from ORM objects (`from_attributes=True`). This keeps the API contract explicit and reduces manual response shaping.

## Follow-ups

Introduce Alembic migrations, move media bytes to object storage (keeping only metadata + URL in Postgres), and add upload safety controls (size limits, content-type allowlist, and a streaming upload path for large files).
