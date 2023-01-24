from fastapi import APIRouter
from webapps import auth
# from webapps import chat
from webapps import chat2
from webapps import videos
from webapps import files

api_router = APIRouter()

api_router.include_router(auth.router, tags=["Auth"])
api_router.include_router(chat2.router, prefix="/chats", tags=["chat"])
api_router.include_router(videos.router, prefix="/videos", tags=["videos"])
api_router.include_router(files.router, prefix="/videos", tags=["videofiles"])