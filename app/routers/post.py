from itertools import groupby
from statistics import mode
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from .. import models,schema,utils,oauth2
from sqlalchemy.orm import Session
from ..database import engine,get_db
from typing import Optional,List
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=[
    'Posts'
    ]
)
# @router.get("/",response_model=List[schema.Post])
@router.get("/",response_model=List[schema.Postout])
def get_posts(db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user),limit: int  =10,
    skip:int = 0,search:Optional[str] = ""):
    print(limit)
    results = db.query(models.Post,func.count(models.Votes.post_id).label("likes")).join(models.Votes,models.Votes.post_id == models.Post.id,isouter=True).group_by(
        models.Post.id
    ).all()
    print(results)
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    print(posts)
    return posts


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schema.Post)
def create_posts(post: schema.PostCreate,db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    print(current_user.email)
    new_post= models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}")
def get_post(id: int,db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):


    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post =  db.query(models.Post,func.count(models.Votes.post_id).label("likes")).join(models.Votes,models.Votes.post_id == models.Post.id,isouter=True).group_by(
        models.Post.id
    ).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail= {"message": f"post with the id: {id} was not found"})
    
    print(post)
    return post


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    print(current_user)

    delete_post_qurey = db.query(models.Post).filter(models.Post.id == str(id))
    post = delete_post_qurey.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={"message":f"post was not found with id: {id}"})
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform this request")

    delete_post_qurey.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}")
def update_post(id:int,updated_post: schema.PostUpdate,db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE post SET title = %s,content = %s,published=%s WHERE id = %s RETURNING * """,(post.title,post.content,post.published,str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_qurey= db.query(models.Post).filter(models.Post.id == str(id))
    post = post_qurey.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={"message":f"post was not found with id: {id}"})
        
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform this request")

    post_qurey.update(updated_post.dict(),synchronize_session=False)
    db.commit()

    return post_qurey.first()