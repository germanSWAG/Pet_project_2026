from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from datetime import datetime, timedelta, timezone
from app.settings.config import settings
from jose import JWTError, jwt, ExpiredSignatureError

def hash_password(password):
    user_hash = PasswordHasher().hash(password)
    return user_hash



def verify_password(hash, password):
    try:
        result = PasswordHasher().verify(hash, password)
        return result
    except VerifyMismatchError:
        return False


def create_token(data : dict) -> str:
    access_payload = data.copy()
    access_expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_payload.update({"exp": access_expire, "type": "access"})
    access_token = jwt.encode(
        access_payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM)

    refresh_expire = datetime.now(timezone.utc) + timedelta(days=30)
    refresh_payload = {"sub" : data.get("sub"),"exp" : refresh_expire,"type": "refresh"}
    
    refresh_token = jwt.encode(
        refresh_payload, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM)


    return {"access_token" : access_token,
            "refresh_token": refresh_token}




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