from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import engine, get_db
from ..schemas import PostCreate, Post, Schemas, Usercreate, UserOut
from ..oauth2 import *
from sqlalchemy import func
from typing import List, Optional
router = APIRouter(
    prefix="/sql",
    tags=["Posts"]
)


@router.post("/", response_model=Schemas)
def sql_post(post: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):

    print(current_user.email)
    new_post = models.Post(**post.dict(), owner_id=current_user.id)
    # new_post = models.Post(
    # title=post.title, content=post.content, published=post.published)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/{id}", response_model=schemas.PostVote)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):

   # post_ = db.query(models.Post).filter(models.Post.id == id)
    post_ = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id)
    print(post_)

    if post_.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not Authorised to perform requested operation")

    post_.delete(synchronize_session=False)
    db.commit()
    return {"Deleted"}


@router.get("/get", response_model=List[schemas.PostVote])
def test_posts(db: Session = Depends(get_db), current_user: int = Depends(get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    """posts = db.query(models.Post).filter(
        models.Post.owner_id == current_user.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()"""
    result_ = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    print(result_)
    return result_
