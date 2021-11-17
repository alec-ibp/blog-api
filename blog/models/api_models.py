# Python
from typing import Optional

# Pydantic
from pydantic import BaseModel
from pydantic.fields import Field


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