from jose import jwt, JWTError
from datetime import datetime, timedelta
from . import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .config import Settings

setting=Settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')
SECRET_KEY = setting.secret_key
ALGORITHM = setting.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = setting.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credential_exception):
    print("Starting to verify token...")  # Start of verification process
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("Decoded payload:", payload)  # Log the decoded payload
        user_id: int = payload.get("user_id")
        print("User ID:", user_id)  # Log the user ID extracted from the payload
        
        if user_id is None:
            print("User ID is None, raising credential_exception")  # Log when user ID is None
            raise credential_exception
        
        print("Creating token_data...")  # Indicate we're creating token_data
        token_data = schemas.TokenData(id=user_id)  # Create token_data
        print("Token data created:", token_data)  # Log the created token_data
        return token_data  # Return the token_data
    except JWTError:
        print("JWTError occurred")  # Log if there was a JWT error
        raise credential_exception  # Raise the credential exception if JWTError occurs



def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # Try to decode the token
    user = verify_access_token(token, credential_exception)
    print("Authenticated user:", user)  # Add this print to check user data
    return user

