from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    name: str
    email: str
    password: str
    
    class Config:
        from_attributes = True


class ShowUser(BaseModel):
    name: str
    email: str
    
    class Config:
        from_attributes = True

class BlogSchema(BaseModel):
    title: str
    body: str
    user_id: int
    
    class Config:
        from_attributes = True

class ShowBlog(BaseModel):
    title: str
    body: str
    owner: Optional[ShowUser]
        
    class Config:
        from_attributes = True

