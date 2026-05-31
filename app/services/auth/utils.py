from datetime import datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import get_config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def _jwt_settings():
    config = get_config()
    return (
        config["jwt_secret_key"],
        config["jwt_algorithm"],
        config["access_token_expire_minutes"],
    )


def create_access_token(data: dict):
    secret_key, algorithm, expire_minutes = _jwt_settings()
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expire_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_key, algorithm=algorithm)


def decode_access_token(token: str):
    secret_key, algorithm, _ = _jwt_settings()
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return payload
    except JWTError:
        return None
