from fastapi import FastAPI
from . import models
from .database import engine
from .routes import posts,users,auth,vote
models.base.metadata.create_all(bind=engine)
from .config import Settings
from fastapi.middleware.cors import CORSMiddleware

settings=Settings()

myapp= FastAPI()
origins=["*"]
myapp.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
store_posts=[]

# while(True):
#     try:
#         conn=psycopg2.connect(host='localhost',database='fastapiprojectserver',user='postgres',password='2506',cursor_factory=RealDictCursor)
#         cursor=conn.cursor()
#         print("Sucessfully connected to database")
#         break

#     except Exception as error:
#         print("Failed to connect to database")
#         print("Error: ",error)
#         time.sleep(2)

myapp.include_router(posts.router)
myapp.include_router(users.router)
myapp.include_router(auth.router)
myapp.include_router(vote.router)

@myapp.get("/")
def print_hello():
    return{"message":"changed"}

#automated documantation
# url/docs or url/redoc

#User Registration

