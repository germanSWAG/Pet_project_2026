from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from datetime import datetime, timedelta, timezone
from app.settings.config import settings
from jose import JWTError, jwt, ExpiredSignatureError
from exception import TokenExpiredError, TokenInvalidError, JWTGenerationError
import hashlib
import secrets

def password_hashing(password):
    user_hash = PasswordHasher().hash(password)
    return user_hash



def verify_password(hash, password):
    try:
        result = PasswordHasher().verify(hash, password)
        return result
    except VerifyMismatchError:
        return False


def generate_access_token(data : dict) -> str:
    try:
        access_payload = {
        **data,
        "exp" : datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        "type" : "access"

    }
        access_token = jwt.encode(
        access_payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM)
    except Exception as e:
        raise JWTGenerationError("Ошибка при генерации jwt токена") from e
    return access_token


            

def verify_token(token : str) -> int:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        return payload["sub"]
    except ExpiredSignatureError as e:
        raise TokenExpiredError("Срок действия токена истек") from e
    except JWTError as e:
        raise TokenInvalidError("Неверный токен или нарушена структура") from e

def hash_refresh_token(token : str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def generate_refresh_token() -> str:
    return secrets.token_urlsafe(64)


