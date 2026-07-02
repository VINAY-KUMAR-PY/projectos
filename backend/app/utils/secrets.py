from __future__ import annotations

import base64
import hashlib

from cryptography.fernet import Fernet, InvalidToken

from app.config.settings import settings


SECRET_PREFIX = "fernet:"


def _fernet() -> Fernet:
    digest = hashlib.sha256(settings.secret_key.encode("utf-8")).digest()
    key = base64.urlsafe_b64encode(digest)
    return Fernet(key)


def encrypt_secret(value: str | None) -> str | None:
    if not value:
        return value
    if value.startswith(SECRET_PREFIX):
        return value
    token = _fernet().encrypt(value.encode("utf-8")).decode("ascii")
    return f"{SECRET_PREFIX}{token}"


def decrypt_secret(value: str | None) -> str | None:
    if not value:
        return value
    if not value.startswith(SECRET_PREFIX):
        return value
    encrypted = value.removeprefix(SECRET_PREFIX).encode("ascii")
    try:
        return _fernet().decrypt(encrypted).decode("utf-8")
    except InvalidToken:
        return None
