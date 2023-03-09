from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(Post):
    pass


class PostUpdate(Post):
    pass


class Usercreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class Userlogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Schemas(Post):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True


class PostVote(BaseModel):
    Post: Schemas
    votes: int

    class Config:
        orm_mode = True


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
