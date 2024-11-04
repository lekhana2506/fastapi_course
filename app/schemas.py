from pydantic import BaseModel,EmailStr,Field
from typing import Optional
class Response(BaseModel):
    title:str
    content:str
    is_published:bool

    class Config:
            orm_mode = True

class UserCreate(BaseModel):
     email:EmailStr
     password:str

class UserResponse(BaseModel):
     id:int
     email:EmailStr

     class Config:
            orm_mode = True

class UserLogin(BaseModel):
     email:EmailStr
     password:str

class Post(BaseModel):
    title:str
    content:str
    is_published: bool = False
    
    class Config:
        orm_mode = True

class CreatePost(Post):
    pass

class RetrievedPost(Post):
     owner_id:int
     owner:UserResponse

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[int]=None

class Vote(BaseModel):
     post_id:int
     direction: int = Field(..., ge=0, le=1)  # Use Field with constraints instead

class PostOut(BaseModel):
     Post:Post
     votes:int

     
