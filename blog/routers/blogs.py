from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..schemas import ShowBlog, Blog
from ..database import get_db
from .. import models


router = APIRouter(
    tags=['blogs']
)

@router.get('/',status_code=status.HTTP_200_OK, response_model=list[ShowBlog])
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@router.post('/',status_code=status.HTTP_201_CREATED, response_model=ShowBlog)
def create_blog(request: Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, creator_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id:int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} is not available")
    blog.delete(synchronize_session=False)
    db.commit()
    return {'data':'done'}

@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED, response_model=ShowBlog)
def update_blog(id:int, request: Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} is not available")
    blog.update({'title':request.title, 'body':request.body},synchronize_session=False)
    db.commit()
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    return blog

@router.get('/{id}',status_code=status.HTTP_200_OK, response_model=ShowBlog)
def show_blog(id:int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        return HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} is not available")
    return blog