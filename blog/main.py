# Python
import re
from typing import List

# Path
from models.db_models import PostDB, UserDB
from models.api_models import Post, UserIn, UserBase
from database import SessionLocal, Base, engine
from hashing import Hash

# SQLAlchemy
from sqlalchemy.orm import Session

# FastAPI
from fastapi import FastAPI, Depends
from fastapi import HTTPException, status
from fastapi import Body, Path, Query


Base.metadata.create_all(engine)
app = FastAPI()


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Blog 
@app.post(
    path='/blog',
    status_code=status.HTTP_201_CREATED)
def create_post(post: Post = Body(...), db: Session = Depends(get_db)):
    
    new_post = PostDB(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post
    

@app.get(
    path='/blog',
    response_model=List[Post],
    status_code=status.HTTP_200_OK)
def show_all_posts(db: Session = Depends(get_db)):
    posts = db.query(PostDB).all()

    return posts


@app.get(
    path='/blog/{id}',
    response_model=Post,
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


@app.delete(
    path='/blog/{id}',
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


@app.put(
path='/blog/{id}', 
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

# User
@app.post(
    path='/user',
    response_model=UserBase)
def create_user(user: UserIn = Body(...), db : Session = Depends(get_db)):

    user.password = Hash.hash_password(user.password)

    new_user = UserDB(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
    

@app.get(
    path='/user/{id}',
    response_model=UserBase)
def show_a_user(
    id: int = Path(
        ...,
        ge=0
    ),
    db: Session = Depends(get_db)
    ):

    user = db.query(UserDB).filter(
        UserDB.id == id
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user does't exist"
        )
    
    return user