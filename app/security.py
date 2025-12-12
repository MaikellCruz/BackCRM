# security.py
import hashlib
import os
import hmac
import binascii
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from pydantic import BaseModel

SECRET_KEY = "sua-chave-secreta-super-dificil"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Simple PBKDF2-SHA256 helper implementation (avoids passlib/bcrypt issues).
# Format returned: pbkdf2_sha256$<iterations>$<salt_hex>$<hash_hex>

_PBKDF2_ITERATIONS = 180_000
_SALT_BYTES = 16


def _normalize_password(s: str, limit: int | None = None) -> bytes:
    """Normalize password to UTF-8 bytes and optionally truncate to `limit` bytes.

    We return bytes because hashlib.pbkdf2_hmac works on bytes.
    """
    b = s.encode("utf-8")
    if limit is None or len(b) <= limit:
        return b
    return b[:limit]


def get_password_hash(password: str) -> str:
    """Hash a password using PBKDF2-HMAC-SHA256 and return encoded string."""
    pwd = _normalize_password(password)
    salt = os.urandom(_SALT_BYTES)
    dk = hashlib.pbkdf2_hmac("sha256", pwd, salt, _PBKDF2_ITERATIONS)
    return f"pbkdf2_sha256${_PBKDF2_ITERATIONS}${binascii.hexlify(salt).decode()}${binascii.hexlify(dk).decode()}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a stored PBKDF2-SHA256 hash string."""
    try:
        algo, iters_s, salt_hex, dk_hex = hashed_password.split("$")
        if algo != "pbkdf2_sha256":
            # Unsupported algorithm
            return False
        iterations = int(iters_s)
        salt = binascii.unhexlify(salt_hex)
        expected = binascii.unhexlify(dk_hex)
    except Exception:
        return False

    pwd = _normalize_password(plain_password)
    computed = hashlib.pbkdf2_hmac("sha256", pwd, salt, iterations)
    return hmac.compare_digest(computed, expected)

def create_access_token(data: dict):
    to_encode = data.copy()
    # Utiliza o método timezone-aware recomendado
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

class TokenData(BaseModel):
    email: str | None = None
    role: str | None = None