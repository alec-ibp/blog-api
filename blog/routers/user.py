# Path
from database import get_db
from models.api_models import UserBase, UserIn, ShowUser
from repository import user

# SQLAlchemy
from sqlalchemy.orm import Session

# FastAPI
from fastapi import APIRouter, Depends
from fastapi import status
from fastapi import Body, Path


router = APIRouter(
    prefix='/user',
    tags=['user']
)


@router.post(
    path='/',
    response_model=UserBase,
    status_code=status.HTTP_201_CREATED)
def create_user(in_user: UserIn = Body(...), db : Session = Depends(get_db)):
    return user.create(in_user, db)
    

@router.get(
    path='/{id}',
    response_model=ShowUser,
    status_code=status.HTTP_200_OK)
def show_a_user(
    id: int = Path(
        ...,
        ge=0
    ),
    db: Session = Depends(get_db)
    ):

    return user.get(id, db)
