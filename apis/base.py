from fastapi import APIRouter
from apis.version1 import users
from apis.version1 import login
from apis.version1 import videos
# from apis.version1 import chat

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(login.router, prefix="/login", tags=["login"])
# api_router.include_router(chat.router, prefix="/apis/chat", tags=["chat"])
api_router.include_router(videos.router, prefix="/api_videos", tags=["api_videos"])