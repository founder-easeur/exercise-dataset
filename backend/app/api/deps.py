"""FastAPI dependencies: DB session + admin API-key auth."""
from __future__ import annotations

import hmac

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.config import settings
from app.db import SessionLocal, get_db


def require_admin(x_api_key: str | None = Header(default=None)) -> str:
    """Admin endpoints require a valid API key (X-API-Key header)."""
    if not x_api_key or not hmac.compare_digest(x_api_key, settings.admin_api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing X-API-Key header",
        )
    return "admin"
