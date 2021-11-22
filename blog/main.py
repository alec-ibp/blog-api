# Path
from database import Base, engine
from routers import post, user, authentication

# FastAPI
from fastapi import FastAPI


Base.metadata.create_all(engine)
app = FastAPI()

app.include_router(authentication.router)
app.include_router(post.router)
app.include_router(user.router)
