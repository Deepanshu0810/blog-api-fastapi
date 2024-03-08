from fastapi import APIRouter, status, Depends, HTTPException
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas import User, ShowUser
from ..hashing import Hash
from .. import models

router = APIRouter(
    prefix='/user',
    tags=['users']
)

@router.post('/',status_code=status.HTTP_201_CREATED, response_model=ShowUser)
def create_user(request: User, db: Session = Depends(get_db)):
    hashed_password = Hash.bcrypt(request.password)
    new_user = models.User(username=request.username, email=request.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}',status_code=status.HTTP_200_OK, response_model=ShowUser)
def get_user(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} is not available")
    return user