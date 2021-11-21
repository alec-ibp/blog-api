# Python
from typing import List

# Path
from models.api_models import Post, ShowPost
from models.db_models import PostDB
from database import get_db

# SQLAlchemy
from sqlalchemy.orm import Session

# FastAPI
from fastapi import APIRouter, Depends
from fastapi import status, HTTPException
from fastapi import Body, Path


router = APIRouter(
    prefix='/blog',
    tags=['blog']
)


@router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,)
def create_post(post: Post = Body(...), db: Session = Depends(get_db)):
    
    post_dict = post.dict()
    post_dict['user_id'] = 1 
    new_post = PostDB(**post_dict)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get(
    path='/',
    response_model=List[ShowPost],
    status_code=status.HTTP_200_OK)
def show_all_posts(db: Session = Depends(get_db)):
    posts = db.query(PostDB).all()

    return posts


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

    post = db.query(PostDB).filter(
        PostDB.id == id
    ).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The post {id} doesn't exist!")
    
    return post


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

    db_post = db.query(PostDB).filter(
        PostDB.id == id)
    
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"the post {id} doesn't exist!"
        )
    
    db_post.delete(synchronize_session=False)
    db.commit()

    return None


@router.put(
path='/{id}',
tags=['blog'], 
status_code=status.HTTP_202_ACCEPTED) 
def update_a_post(
    id: int = Path(
        ...,
        ge=0
    ),
    post: Post = Body(...),
    db: Session = Depends(get_db)
    ):

    db_post = db.query(PostDB).filter(
        PostDB.id == id)

    if not db_post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"the post {id} doesn't exist!"
        )

    db_post.update(post.dict())
    db.commit()

    return None