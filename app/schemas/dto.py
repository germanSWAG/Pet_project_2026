from pydantic import BaseModel, EmailStr

class RegisterDTO(BaseModel):
    username : str
    email : EmailStr
    hash_password : str


class LoginDTO(BaseModel):
    email : EmailStr
    hash_password : str
