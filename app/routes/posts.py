from ..import models,schemas
from fastapi import FastAPI,Depends,APIRouter,HTTPException,status
from fastapi.params import Body
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..database import get_db
from .. import oauth2
from typing import Optional

router=APIRouter()

# def get_post_by_id(id):
#     for p in store_posts:
#         if p.id==id:
#             return p
        
# def find_post_id(id):
#     for index, post in enumerate(store_posts):
#         if post.id == id:
#             return index


@router.get("/testing")
def test_post(db: Session=Depends(get_db)):
    posts=db.query(models.Post).all()
    return posts

#basic get
@router.get("/createposts",response_model=list[schemas.PostOut])
def print_hello_world(db:Session=Depends(get_db),current_user: int = Depends(oauth2.get_current_user),limit:int=10,skip:int=0,search:Optional[str]=""):
    # cursor.execute(""" select * from posts""")
    # collected_posts=cursor.fetchall()
    # print(collected_posts)

    # #to get only posts of the user logged in 
    # collected_posts=db.query(models.Post).filter(models.Post.owner_id==current_user.id)
    # if not collected_posts:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    # return collected_posts
    print("starting to collect")
    # collected_posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    results=db.query(models.Post,func.count(models.Votes.post_id).label("votes")).join(models.Votes,models.Votes.post_id==models.Post.id,isouter=True).group_by(models.Post.id).all()
    print("collected")
    # formatted_results = [
    #     {
    #         "id": post.id,
    #         "title": post.title,
    #         "content": post.content,
    #         "votes_count": votes_count
    #     }
    #     for post, votes_count in results
    # ]
    # print(formatted_results)
    # return formatted_results

    return results

#basic put 
@router.post("/")
def get_post_message(post:dict=Body(...)):
    return post

#defining the schema of the info to be retrived
@router.post("/createposts", response_model=schemas.RetrievedPost)
def create_post(post: schemas.CreatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print("Creating post with data:", post)
    new_post = models.Post(owner_id=current_user.id,**post.dict())  # convert post to dict, unpack and extract fields and pass it to new_post
    print("New post created:", new_post)
    db.add(new_post)
    print("New post added to the session.")
    db.commit()
    print("Changes committed to the database.")
    db.refresh(new_post)
    print("Post refreshed with new data.")
    # print(new_post.title)
    # print(new_post.content)
    # print(new_post.is_published)
    return new_post

#creating an array to store the data
# @router.post("/createposts")
# def store_posts_in_array(post:schemas.Post):
#     store_posts.routerend(post)
#     return "Array updated"

# @router.get("/createposts")
# def return_posts():
#     return{"posts":store_posts}

#getting post using id
@router.get("/createposts/{id}",response_model=schemas.PostOut)
def get_post_using_id(id:int,db:Session=Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
#    cursor.execute(""" select * from posts where id=%s returning * """,(str(id)))
#    post=cursor.fetchone()
    # posts=db.query(models.Post).filter(models.Post.id==id).first()
    # if not posts:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    # if posts.owner_id!=current_user.id:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    # return posts

    results=db.query(models.Post,func.count(models.Votes.post_id).label("votes")).join(models.Votes,models.Post.id==models.Votes.post_id,isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    if not results:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return results


#deleting posts   
@router.delete("/createposts/{id}")
def delete_post_using_id(id:int,db:Session=Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""delete from posts where id =%s returning * """,(str(id)))
    # conn.commit()
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    # print(post.owner_id)
    # print(current_user.id)
    # valid_user_id=post.id
    if post.owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    post_query.delete(synchronize_session=False)
    db.commit()
    return("deleted sucessfully")


#updating a post with given id
@router.put("/createposts/{id}",response_model=schemas.RetrievedPost)
def update_posts(id:int,post:schemas.Post,db:Session=Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""update posts set title=%s ,content=%s,is_published=%s where id=%s returning * """,(post.title,post.content,post.is_published,str(id)))
    # updated_post=cursor.fetchone()
    # conn.commit()
    post_updated_query=db.query(models.Post).filter(models.Post.id==id)
    current_post=post_updated_query.first()
    if not current_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if current_post.owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    post_updated_query.update(post.dict(),synchronize_session=False)
    db.commit()
    return post_updated_query.first()


#note : 
# post_updated_query = db.query(models.Post).filter(models.Post.id == id)
# is the same as cursor.execute(""" select * from posts where id=%s""",(str(id))), doesnt return anything, its just the query
# where as 
# post_updated_query = db.query(models.Post).filter(models.Post.id == id).first()
# is the same as cursor.execute(""" select * from posts where id=%s returning * """,(str(id))), returns the first and only occurance of the object with that id
