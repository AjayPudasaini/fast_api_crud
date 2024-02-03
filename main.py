from fastapi import FastAPI
from database.database import engine
from models.posts import Base
from routers.posts import router as posts_router
from routers.users import  router as users_router
from routers.auth import router as auth_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(posts_router)
app.include_router(users_router)
app.include_router(auth_router)