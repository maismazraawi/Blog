from fastapi import FastAPI, Depends, HTTPException, status, Response
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from blog import models, schemas, database
from blog.database import engine, SessionLocal
from blog.schemas import BlogSchema, ShowBlog, User
from typing import List
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import joinedload


app = FastAPI()

# after using alembic no need for it:
#Create tables in the database
#models.Base.metadata.create_all(bind=engine)

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/user', tags=['users'], response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(id=request.id , name=request.name, email=request.email, password=request.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    

@app.get('/users', tags=['users'], response_model=List[schemas.User], status_code=status.HTTP_202_ACCEPTED)
def show_all_users(db: Session= Depends(get_db)):
    users = db.query(models.User).all()
    return jsonable_encoder(users)


@app.post('/blog', tags=['blogs'], response_model=schemas.ShowBlog, status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.BlogSchema, db: Session = Depends(get_db)):
    new_blog = models.Blog(
        title=request.title, 
        body=request.body, 
        user_id=request.user_id
        )
    
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blogs', tags=['blogs'], response_model=List[schemas.ShowBlog], status_code=status.HTTP_202_ACCEPTED)
def show_all_blogs(db: Session= Depends(get_db)):
    blogs = db.query(models.Blog).options(joinedload(models.Blog.owner)).all()
    return jsonable_encoder(blogs)


@app.get('/blog/{id}', tags=['blogs'], response_model=schemas.ShowBlog, status_code=status.HTTP_202_ACCEPTED)
def show(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).options(joinedload(models.Blog.owner)).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'Blog with id {id} is not available')
    return jsonable_encoder(blog)


