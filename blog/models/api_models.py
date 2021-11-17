# Python
from typing import Optional

# Pydantic
from pydantic import BaseModel
from pydantic.fields import Field
from pydantic.networks import EmailStr


class Post(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=64
    )

    body: str = Field(
        ...,
        min_length=1,
        max_length=256
    )

    published: Optional[bool] = Field(
        default=False
    )

    
    class Config():
        orm_mode = True


class User(BaseModel):
    first_name: str = Field(
        ...,
        min_length=2,
        max_length=32
    )

    last_name: str = Field(
        ...,
        min_length=2,
        max_length=32
    )

    username: str = Field(
        ...,
        min_length=2,
        max_length=64
    )

    email: EmailStr = Field(...)

    password: str = Field(
        ...,
        min_length=8
    )
