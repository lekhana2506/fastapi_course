from fastapi import FastAPI,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from .. import database,models,oauth2,schemas

router=APIRouter(
    tags=['Votes']
)

@router.post("/votes",status_code=status.HTTP_201_CREATED)
def vote(votes:schemas.Vote,db:Session=Depends(database.get_db),current_user:int=Depends(oauth2.get_current_user)):
    #check if posts exists
    post=db.query(models.Post).filter(models.Post.id==votes.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    vote_query=db.query(models.Votes).filter(models.Votes.post_id==votes.post_id,models.Votes.user_id==current_user.id)
    voted=vote_query.first()
    vote_dir=votes.direction
    if vote_dir==1:
        if voted:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)
        new_vote=models.Votes(post_id=votes.post_id,user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return "Post Liked!"
    elif vote_dir==0:
        if not voted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        vote_query.delete(synchronize_session=False)
        db.commit()
        return("Sucessfully deleted vote")
        
