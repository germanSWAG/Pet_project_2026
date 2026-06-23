from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator
import re

class UserAdd(BaseModel):
    username: str = Field(max_length=128)
    email : EmailStr
    password : str = Field(min_length=8, max_length=64)
    @field_validator('password')
    @classmethod
    def password_valide(cls, v : str) -> str:
        capital_letters = bool(re.search(r"[A-Z]", v))
        special_characters = bool(re.search(r"[^\w\s]", v))
        if not ( capital_letters or special_characters):
            raise ValueError("Пароль должен содержать хотя бы одну заглавную букву или спец-символ")
        return v
        
        

class UserGet(BaseModel):
    email : EmailStr
    hash_password : str = Field(min_length=8, max_length=64)



class UserOut(BaseModel):
    id : int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)

