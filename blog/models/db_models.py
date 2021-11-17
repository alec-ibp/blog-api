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


class UserDB(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)

    first_name = Column(String(32))
    last_name = Column(String(32))
    username = Column(String(64))
    email = Column(String(128))
    password = Column(String(128))


    def __init__(self, first_name, last_name, username, email, password) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = password
