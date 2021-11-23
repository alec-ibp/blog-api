# Python
from typing import List

# Path
from models.api_models import Post, ShowPost, UserBase
from database import get_db
from repository import post
from oauth2 import get_current_user

# SQLAlchemy
from sqlalchemy.orm import Session

# FastAPI
from fastapi import APIRouter, Depends
from fastapi import status
from fastapi import Body, Path


router = APIRouter(
    prefix='/blog',
    tags=['blog']
)


@router.post(
    path='/',
    response_model=Post,
    status_code=status.HTTP_201_CREATED,)
def create_post(in_post: Post = Body(...), db: Session = Depends(get_db)):
    return post.create(in_post, db)


@router.get(
    path='/',
    response_model=List[ShowPost],
    status_code=status.HTTP_200_OK)
def show_all_posts(db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return post.get_all(db)


@router.get(
    path='/{id}',
    response_model=ShowPost,
    status_code=status.HTTP_200_OK)
def show_a_post(
    id: int = Path(
        ...,
        ge=1
    ),
    db: Session = Depends(get_db)
    ):

    return post.get(id, db)


@router.delete(
    path='/{id}',
    status_code=status.HTTP_204_NO_CONTENT)
def delete_a_post(
    id: int = Path(
        ...,
        ge=1
    ),
    db: Session = Depends(get_db)
    ):

    return post.delete(id, db)


@router.put(
path='/{id}',
status_code=status.HTTP_202_ACCEPTED) 
def update_a_post(
    id: int = Path(
        ...,
        ge=0
    ),
    in_post: Post = Body(...),
    db: Session = Depends(get_db)
    ):

    return post.update(id, in_post, db)