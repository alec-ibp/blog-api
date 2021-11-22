# Path
from models.api_models import UserIn
from models.db_models import UserDB
from hashing import Hash

# SQLAlchemy
from sqlalchemy.orm import Session

# FastAPI
from fastapi import HTTPException, status


def create(user: UserIn, db: Session):
    user.password = Hash.hash_password(user.password)

    new_user = UserDB(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get(id: int, db: Session):
    user = db.query(UserDB).filter(
        UserDB.id == id
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user does't exist"
        )
    
    return user