import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, models, oauth2,schemas
import logging
from passlib.context import CryptContext

# Create a CryptContext with bcrypt as the hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter(tags=["Authentication"])
logger = logging.getLogger("uvicorn.error")

@router.post("/login",response_model=schemas.Token)
def login(user_credential: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    try:
        valid_user = db.query(models.User).filter(models.User.email == user_credential.username).first()
        if not valid_user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid email or password")
        
        valid_pwd = pwd_context.verify(user_credential.password, valid_user.password)
        if not valid_pwd:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid email or password")
        print(user_credential.username)
        print(user_credential.password)
        access_token = oauth2.create_access_token(data={"user_id": valid_user.id})
        return {"access_token": access_token, "token_type": "bearer"}
    
    except Exception as e:
        logger.error(f"Error during login: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
