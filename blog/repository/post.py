# Path
from models.db_models import PostDB
from models.api_models import Post
# SQLAlchemy
from sqlalchemy.orm import Session

# FastAPI
from fastapi import HTTPException, status


def get_all(db: Session):
    posts = db.query(PostDB).all()
    return posts


def get(id: int, db: Session):
    post = db.query(PostDB).filter(
        PostDB.id == id
    ).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The post {id} doesn't exist!")
    
    return post


def create(post: Post, db: Session):
    post_dict = post.dict()
    post_dict['user_id'] = 1 
    new_post = PostDB(**post_dict)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


def delete(id: int, db: Session):
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


def update(id:int, post: Post, db: Session):
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