# Python
from typing import Optional, List

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


class UserBase(BaseModel):
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

    
    class Config():
        orm_mode = True


class UserIn(UserBase):
    password: str = Field(
        ...,
        min_length=8
    )


class LoginUser(BaseModel):
    username: str = Field(
        ...,
        min_length=2,
        max_length=64
    )

    password: str = Field(
        ...,
        min_length=8
    )

class ShowUser(UserBase):
    posts: List[Post] = Field(...)


class ShowPost(Post):
    author: ShowUser = Field(...)


class Token(BaseModel):
    access_token: str = Field(...)
    token_type: str = Field(...)


class TokenData(BaseModel):
    email: Optional[EmailStr]