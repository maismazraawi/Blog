from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel

# Initialize the SQLAlchemy Base
Base = declarative_base()

# SQLAlchemy model
class Blog(Base):
    __tablename__ = 'blogs'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)

    # Pydantic Config for response validation directly from ORM models
    class Config:
        model_config = {"from_attributes": True}


# Pydantic schema for Blog
class BlogSchema(BaseModel):
    id: int
    title: str
    body: str

    # Configuration to allow creating a schema from ORM models
    model_config = {"from_attributes": True}
