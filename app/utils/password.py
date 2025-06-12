import bcrypt


def hash_password(password: str) -> bytes:
    """Hash a password"""

    hashed_bytes = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed_bytes


def check_password(password: str, hashed_password: bytes) -> bool:
    """Check password against hashed password"""

    check = bcrypt.checkpw(password.encode("utf-8"), hashed_password)
    return check
