# Path
from database import Base

# SQLAlchemy
from sqlalchemy import Column, String, Integer, Text, Boolean
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship


class PostDB(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(64), nullable=False)
    body = Column(Text, nullable=False)
    published = Column(Boolean, nullable=False, default=False)
    user_id = Column("user_id", Integer, ForeignKey("users.id"), nullable=False)

    author = relationship("UserDB", back_populates='posts')

    def __init__(self, title, body, published, user_id) -> None:
        self.title = title
        self.body = body
        self.published = published
        self.user_id = user_id


class UserDB(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)

    first_name = Column(String(32), nullable=False)
    last_name = Column(String(32), nullable=False)
    username = Column(String(64), nullable=False)
    email = Column(String(128), nullable=False, unique=True)
    password = Column(String(128), nullable=False)

    posts = relationship("PostDB", back_populates="author")

    def __init__(self, first_name, last_name, username, email, password) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = password
