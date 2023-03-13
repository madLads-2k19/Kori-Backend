from passlib.context import CryptContext

from kori.app.core.config import Settings

config = Settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: bytes, hashed_password: bytes) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: bytes) -> bytes:
    return pwd_context.hash(password)
