# Path
from database import Base

# SQLAlchemy
from sqlalchemy import Column, String, Integer, Text, Boolean


class PostDB(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(64))
    body = Column(Text)
    published = Column(Boolean)


    def __init__(self, title, body, published) -> None:
        self.title = title
        self.body = body
        self.published = published
