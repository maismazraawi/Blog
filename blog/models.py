from fastapi import HTTPException
from sqlalchemy import Column, Integer, String, ForeignKey
from blog.database import Base
from sqlalchemy.orm import relationship
from passlib.context import CryptContext
import re


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Blog(Base):
    __tablename__ = 'blogs'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String)
    body = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    
    owner = relationship("User", back_populates="blogs")

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    blogs = relationship("Blog", back_populates="owner")
    
    
    # Validate password format before setting it
    @staticmethod
    def validate_password(password: str):
        # Password must be at least 8 characters long, contain a lowercase letter, uppercase letter, digit, and special character
        password_regex = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')
        if not password_regex.match(password):
            raise HTTPException(
                status_code=400,
                detail="Password must be at least 8 characters long, include one uppercase letter, one lowercase letter, one number, and one special character."
            )
        
    # Hash password before storing it in the database
    def hash_password(self, password: str):
        self.validate_password(password)  # Validate password format
        self.password = pwd_context.hash(password)

    # Verify if the entered password matches the stored password
    def verify_password(self, password: str):
        return pwd_context.verify(password, self.password)