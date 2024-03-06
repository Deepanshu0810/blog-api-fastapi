from fastapi import APIRouter, Depends, status, HTTPException
from ..schemas import UserLogin, Token
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models
from ..hashing import Hash
from ..token import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, timedelta

router = APIRouter(
    tags=['authentication']
)


@router.post('/login')
def login(request: UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")