from ..import models,schemas,utils
from fastapi import FastAPI,Depends,APIRouter
from pydantic import BaseModel
from fastapi.params import Body
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from ..database import get_db,engine


router=APIRouter()
@router.post("/users",response_model=schemas.UserResponse)
def user_login(user:schemas.UserCreate,db:Session=Depends(get_db)):

    #hashing the password
    hashed_pwd=utils.hash(user.password)
    user.password=hashed_pwd

    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/users/{id}",response_model=schemas.UserResponse)
def get_users(id:int,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    return user