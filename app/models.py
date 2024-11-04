from .database import base
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from sqlalchemy.sql.expression import null,text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship

class Post(base):
    __tablename__="posts"
    id=Column(Integer,primary_key=True,nullable=False)
    title=Column(String,nullable=False)
    content=Column(String,nullable=False)
    is_published=Column(Boolean,server_default='TRUE')
    created_at =Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    owner_id=Column(Integer,ForeignKey("users.id",ondelete='CASCADE'),nullable=False)
    owner=relationship("User")

    class Config:
        orm_mode = True

class User(base):
    __tablename__ = "users"
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    class Config:
        orm_mode = True

class Votes(base):
    __tablename__="votes"
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True,nullable=False)
    post_id=Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True,nullable=False)


   


