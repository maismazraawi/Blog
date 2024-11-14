from fastapi import FastAPI, Depends, HTTPException, status, Response
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session, joinedload
from blog import models, schemas, auth, database, oauth2
from blog.database import engine, SessionLocal, get_db
from blog.schemas import BlogSchema, ShowBlog, User
from typing import List
from sqlalchemy.ext.declarative import declarative_base


app = FastAPI()


app.include_router(auth.router)


@app.post('/user', tags=['users'], response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name, 
                           email=request.email)
    
    try:
        new_user.hash_password(request.password)  
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    

@app.get('/users', tags=['users'], response_model=List[schemas.ShowUser], status_code=status.HTTP_202_ACCEPTED)
def show_all_users(db: Session= Depends(get_db), get_current_user:schemas.User = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == get_current_user.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return jsonable_encoder(user)


@app.post('/blog', tags=['blogs'], response_model=schemas.ShowBlog, status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.BlogSchema, db: Session = Depends(get_db), get_current_user:schemas.User = Depends(oauth2.get_current_user)):
    new_blog = models.Blog(title=request.title, 
                           body=request.body, 
                           user_id=get_current_user.id)
    
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blogs', tags=['blogs'], response_model=List[schemas.ShowBlog], status_code=status.HTTP_202_ACCEPTED)
def show_all_blogs(db: Session= Depends(get_db), get_current_user:schemas.User = Depends(oauth2.get_current_user)):
    blogs = db.query(models.Blog).options(joinedload(models.Blog.owner)).filter(models.Blog.user_id == get_current_user.id).all()
    return jsonable_encoder(blogs)


@app.get('/blog/{id}', tags=['blogs'], response_model=schemas.ShowBlog, status_code=status.HTTP_202_ACCEPTED)
def show(id: int, db: Session = Depends(get_db), get_current_user:schemas.User = Depends(oauth2.get_current_user)):
    blog = db.query(models.Blog).options(joinedload(models.Blog.owner)).filter(models.Blog.id == id, models.Blog.user_id == get_current_user.id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'Blog with id {id} is not available or you dont have access to it')
    return jsonable_encoder(blog)


