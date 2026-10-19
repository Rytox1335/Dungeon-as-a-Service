from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-change-me-please-use-32-chars")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = 60

password_hasher = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return password_hasher.verify(password, password_hash)


def create_access_token(player_id: int | None) -> str:
    if player_id is None:
        raise ValueError("player_id is required")
    payload = {
        "sub": str(player_id),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
