from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from .schemas import Blog, BlogSchema, Base
from .database import engine, SessionLocal
from typing import List

app = FastAPI()

# after using alembic no need for it:
#to access metadata and connect it to sql engine
#models.Base.metadata.create_all(bind=engine)

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=status.HTTP_202_ACCEPTED)
def create(request: BlogSchema, db: Session = Depends(get_db)):
    new_blog = Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blogs', status_code=status.HTTP_202_ACCEPTED)
def show(db: Session= Depends(get_db)):
    blogs = db.query(Blog).all()
    return jsonable_encoder(blogs)