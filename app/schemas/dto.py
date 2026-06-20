from pydantic import BaseModel, EmailStr, HttpUrl

class RegisterDTO(BaseModel):
    username : str
    email : EmailStr
    hash_password : str


class LoginDTO(BaseModel):
    email : EmailStr
    hash_password : str



class ItemsDTO(BaseModel):
    brand : str
    model : str
    year : int 
    price : str
    link : HttpUrl
