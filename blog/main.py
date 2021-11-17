# Path'
from models.db_models import PostDB
from models.api_models import Post
from database import SessionLocal, Base, engine

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

@app.post(
    path='/blog',
    status_code=status.HTTP_201_CREATED)
def create_post(post: Post = Body(...), db: Session = Depends(get_db)):
    new_post = PostDB(title=post.title, body=post.body, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post
    