from turtle import right
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from .. import database,schema,models,oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/like",
    tags=['Like']
)


@router.post("/",status_code=status.HTTP_201_CREATED)
def like(like: schema.Like,db: Session = Depends(database.get_db),current_user: int  = Depends(oauth2.get_current_user)):
    post = db.query(models.Votes).filter(models.Post.id == like.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id - {like.post_id} was not found")
    like_qurey = db.query(models.Votes).filter(models.Votes.post_id == like.post_id, models.Votes.user_id == current_user.id)
    found_like = like_qurey.first()
    if(like.dir == 1):
        if found_like:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"User {current_user.id} has alredy like the post")
        new_like = models.Votes(post_id = like.post_id,user_id= current_user.id)
        db.add(new_like)
        db.commit()
        return({"message","Successfully like the post"})
    else:
        if not found_like:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"Like does not exist")
        like_qurey.delete(synchronize_session=False)
        db.commit()

        return{"message":"Successfully unlike the post"}