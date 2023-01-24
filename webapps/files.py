import os
from fastapi import(
    APIRouter, File, UploadFile,
    Depends, Request, Response,
    WebSocket, WebSocketDisconnect,websockets,
    Form, Header, status, HTTPException,
    )
from fastapi.responses import StreamingResponse
from typing import BinaryIO
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi_pagination import Page, add_pagination, paginate
from sqlalchemy.orm import Session
from urllib.parse import quote, unquote
from pathlib import Path
from datetime import datetime

from schemas.users import User
from schemas.videos import VideoItem, UpdateVideo, SearchVideos
from core.config import settings
from apis.version1.login import oauth2_scheme, is_token, get_current_user_from_token
from db.session import get_db

from apis.utils.videos.etc import (
    get_pages, get_etc_keyword
)
from db.repository.videos import (
    get_test2, get_all_videos, get_all_choice, get_all_nys, 
    get_all_videos_random, get_all_choice_random, get_all_nys_random,
    update_video, search_videos, del_video_dbid,
)
from apis.utils.videos.refix import refix_video, del_gif, del_webp, del_viedo
from apis.utils.videos.stream_mp4 import range_requests_response
from core.config import settings

router = APIRouter()
templates = Jinja2Templates(directory='templates')
templates.env.filters['quote'] = quote
templates.env.filters['unquote'] = unquote


router.mount("/static", StaticFiles(directory="static"), name="static")


@router.get('/refix')
def refix_videos(
    request: Request, 
    db: Session=Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
    ):
    
    return templates.TemplateResponse(
        'videos/refix/info.html', {
            'request': request, 
            'items': refix_video(db), 
            'is_token': is_token(token=request.cookies.get('access_token'),db=db),
            'etc_kwd': get_etc_keyword(db),
            }
        )


@router.get("/files/")
async def create_files(
    request: Request,
    db: Session=Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    return templates.TemplateResponse(
        'videos/files/upload.html', {
            "request": request,
            'is_token': is_token(token=request.cookies.get('access_token'),db=db),
            
        }
    )


@router.post("/files/")
async def create_files(
    files: list[bytes] = File(description="Multiple files as bytes"),
):
    return {"file_sizes": [len(file) for file in files]}


@router.post("/uploadfiles/")
async def create_upload_files(
    request: Request,
    files: list[UploadFile] = File(description="Multiple files as UploadFile"),
    db: Session=Depends(get_db),
):
    upload_dir = settings.ROOT_DIR + datetime.now().date().strftime("%Y_%m/")
    if not os.path.exists(upload_dir):
        os.mkdir(upload_dir)
    for file in files:
        contents = await file.read()
        with open(os.path.join(upload_dir, file.filename), "wb") as fp:
            if os.path.exists(fp.name):
                continue
            else:
                fp.write(contents)
        print(os.path.join(upload_dir, file.filename))
    # return {"filenames": [file.filename for file in files]}
    return templates.TemplateResponse(
        'videos/refix/info.html', {
            'request': request, 
            'items': refix_video(db), 
            'is_token': is_token(token=request.cookies.get('access_token'),db=db),
            'etc_kwd': get_etc_keyword(db),
            'filenames': [file.filename for file in files],
            }
        )