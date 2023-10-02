from pickle import TRUE
from turtle import st
from typing import Optional
from pydantic import BaseModel,EmailStr,conint
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    is_published: bool = True

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True



class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    class Config:
        orm_mode = True

class Postout(BaseModel):
    Post: Post
    likes: int
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str




class UserLogin(BaseModel):
    email: EmailStr
    password: str



class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
    
    
class Like(BaseModel):
    post_id: int
    dir: conint(le=1)