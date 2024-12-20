from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    name: str
    email: str
    password: str
    
    class Config:
        from_attributes = True


class ShowUser(BaseModel):
    name: Optional[str]
    email: Optional[str]
    
    class Config:
        from_attributes = True

class BlogSchema(BaseModel):
    title: str
    body: str
    
    class Config:
        from_attributes = True


class Login(BaseModel):
    email: str
    password: str
    

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None