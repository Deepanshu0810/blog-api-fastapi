from fastapi import FastAPI, Depends, status, Response, HTTPException
from .schemas import Blog, ShowBlog, User
from . import models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog',status_code=status.HTTP_201_CREATED, response_model=ShowBlog)
def create_blog(request: Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id:int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} is not available")
    blog.delete(synchronize_session=False)
    db.commit()
    return {'data':'done'}

@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED, response_model=ShowBlog)
def update_blog(id:int, request: Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} is not available")
    blog.update({'title':request.title, 'body':request.body},synchronize_session=False)
    db.commit()
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    return blog

@app.get('/blog',status_code=status.HTTP_200_OK, response_model=list[ShowBlog])
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}',status_code=status.HTTP_200_OK, response_model=ShowBlog)
def show_blog(id:int, response: Response,db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        return HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} is not available")
    return blog

@app.post('/user',status_code=status.HTTP_201_CREATED)
def create_user(request: User, db: Session = Depends(get_db)):
    new_user = models.User(username=request.username, email=request.email, password=request.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user