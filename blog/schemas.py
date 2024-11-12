from pydantic import BaseModel

class BlogSchema(BaseModel):
    id: int
    title: str
    body: str

    class Config:
        from_attributes = True

class ShowBlog(BaseModel):
    title: str
    body: str

    class Config:
        from_attributes = True

class User(BaseModel):
    id: int
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