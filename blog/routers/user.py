# Path
from database import get_db
from models.api_models import UserBase, UserIn, ShowUser
from models.db_models import UserDB
from hashing import Hash

# SQLAlchemy
from sqlalchemy.orm import Session

# FastAPI
from fastapi import APIRouter, Depends
from fastapi import status, HTTPException
from fastapi import Body, Path


router = APIRouter(
    prefix='/user',
    tags=['user']
)


@router.post(
    path='/',
    response_model=UserBase)
def create_user(user: UserIn = Body(...), db : Session = Depends(get_db)):

    user.password = Hash.hash_password(user.password)

    new_user = UserDB(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get(
    path='/{id}',
    response_model=ShowUser)
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
