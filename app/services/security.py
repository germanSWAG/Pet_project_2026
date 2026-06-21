from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from datetime import datetime, timedelta, timezone
from app.settings.config import settings
from jose import JWTError, jwt, ExpiredSignatureError
import hashlib
import secrets

def hash_password(password):
    user_hash = PasswordHasher().hash(password)
    return user_hash



def verify_password(hash, password):
    try:
        result = PasswordHasher().verify(hash, password)
        return result
    except VerifyMismatchError:
        return False


def generate_access_token(data : dict) -> dict:
    access_payload = data.copy()
    access_expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_payload.update({"exp": access_expire, "type": "access"})
    access_token = jwt.encode(
        access_payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM)
   
    


    return {"access_token" : access_token}
            




def verify_token(token : str) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        return payload
    except ExpiredSignatureError as e:
        print(f"Время токена истекло! {e}")
        return None
    except JWTError as e:
        print(f"Токен подделан или нарушена структура {e}")
        return None
    

def hash_refresh_token(token : str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def generate_refresh_token() -> str:
    return secrets.token_urlsafe(64)

