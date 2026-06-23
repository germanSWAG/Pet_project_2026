from pydantic import BaseModel, EmailStr, HttpUrl

class RegisterDTO(BaseModel):
    username : str
    email : EmailStr
    password : str


class LoginDTO(BaseModel):
    email : EmailStr
    password : str



class ItemsDTO(BaseModel):
    brand : str
    model : str
    year : int 
    price : float
    link : HttpUrl


class TokenPair(BaseModel):
    access_token : str
    refresh_token : str