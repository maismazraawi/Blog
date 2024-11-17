from urllib import request
from fastapi import FastAPI, Depends, HTTPException, status, Response
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session, joinedload
from blog import models, schemas, auth, database, oauth2
from blog.database import engine, SessionLocal, get_db
from blog.schemas import BlogSchema, User
from typing import List
from sqlalchemy.ext.declarative import declarative_base


app = FastAPI()


app.include_router(auth.router)


@app.post('/user', tags=['users'], status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email)
    try:
        new_user.hash_password(request.password)  
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user.name and new_user.email
    

@app.get('/users', tags=['users'], response_model=List[schemas.ShowUser], status_code=status.HTTP_202_ACCEPTED)
def show_all_users(db: Session= Depends(get_db)):
    users = db.query(models.User).all()
    return jsonable_encoder(users)


@app.post('/blog', tags=['blogs'], response_model=schemas.BlogSchema, status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.BlogSchema, 
                db: Session = Depends(get_db), 
                current_user:models.User = Depends(oauth2.get_current_user),
                ):
    new_blog = models.Blog(title=request.title, 
                           body=request.body, 
                           user_id=current_user.id)
    
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blogs', tags=['blogs'], response_model=List[schemas.BlogSchema], status_code=status.HTTP_202_ACCEPTED)
def show_all_blogs(db: Session= Depends(get_db)):
    blogs = db.query(models.Blog).options(joinedload(models.Blog.owner)).all()
    return jsonable_encoder(blogs)


@app.get('/blog/{id}', tags=['blogs'], response_model=schemas.BlogSchema, status_code=status.HTTP_202_ACCEPTED)
def show(id: int, db: Session = Depends(get_db), 
         get_current_user:schemas.User = Depends(oauth2.get_current_user),
         ):
    blog = db.query(models.Blog).options(joinedload(models.Blog.owner)).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'Blog with id {id} is not available')
    
    return jsonable_encoder(blog)


@app.patch('/blogs/edit/{blog_id}', tags=['blogs'], status_code=status.HTTP_202_ACCEPTED)
def edit_blog(blog_id:int, request:schemas.BlogSchema, 
              db:Session=Depends(get_db), 
              get_current_user:schemas.User = Depends(oauth2.get_current_user),
              current_user: schemas.User = Depends(oauth2.get_current_user)
              ):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id {id} is not found')
    
    if blog.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to edit this blog")

    blog.title = request.title or blog.title
    blog.body = request.body or blog.body
    db.commit()
    db.refresh(blog)
    return {"message": "Blog updated successfully", "data": blog}

    
@app.delete('/blogs/delete/{blog_id}', tags=['blogs'], status_code=status.HTTP_202_ACCEPTED)
def delete_blog(blog_id:int, 
                db:Session=Depends(get_db), 
                get_current_user:schemas.User = Depends(oauth2.get_current_user),
                current_user: schemas.User = Depends(oauth2.get_current_user)
                ):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id {id} is not found')
    
    if blog.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to edit this blog")

    db.delete(blog)
    db.commit()
    return {'detail': f'Blog with id {id} deleted successfully'}