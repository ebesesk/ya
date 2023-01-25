import os
from fastapi import(
    APIRouter, Depends, Request, Response,
    WebSocket, WebSocketDisconnect,websockets,
    Form, Header, status, HTTPException
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

from schemas.users import User
from schemas.videos import VideoItem, UpdateVideo, SearchVideos
from core.config import settings
from core.security import oauth2_scheme, is_token, get_current_user_from_token
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


@router.get("")
def view_main(request: Request,
              response: Response, 
              db: Session = Depends(get_db),
              current_user: User = Depends(get_current_user_from_token)):
    return templates.TemplateResponse(
        "videos/vmain.html", {
            "request": request,
            "items": get_test2(db)[:16],
            "pages": 1,
            "is_token": is_token(token=request.cookies.get('access_token'),db=db),
            "etc_kwd": get_etc_keyword(db),
        }
    )


@router.get("/all{page}", response_model=Page[VideoItem])
def view_all(
    request: Request, 
    db: Session=Depends(get_db),
    token: str = Depends(oauth2_scheme),
    ):
    items = paginate(get_all_videos(db))
    name = ('all', '?size=' + str(settings._PAGESIZE))
    pages = get_pages(items)
    return templates.TemplateResponse(
        "videos/main.html", {
            "request": request, 
            "items": items, 
            'page_num': {'name': name, 'pages': pages, 'pagesize': settings._PAGESIZE},
            "is_token": is_token(token=request.cookies.get('access_token'),db=db),
            'etc_kwd': get_etc_keyword(db),
            },
        )
 

@router.get("/choice{page}", response_model=Page[VideoItem])
def view_choice(
    request: Request, 
    db: Session=Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
    ):
    
    items = paginate(get_all_choice(db))
    name = ('choice', '?size=' + str(settings._PAGESIZE))
    pages = get_pages(items)
    
    return templates.TemplateResponse(
        "videos/main.html", {
            "request": request, 
            "items": items, 
            'page_num': {'name': name, 'pages': pages, 'pagesize': settings._PAGESIZE},
            "is_token": is_token(token=request.cookies.get('access_token'),db=db),
            'etc_kwd': get_etc_keyword(db),
            },
        )


@router.get("/nys{page}", response_model=Page[VideoItem])
def view_nys(
    request: Request, 
    db: Session=Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
    ):
    
    items = paginate(get_all_nys(db))
    name = ('nys', '?size=' + str(settings._PAGESIZE))
    pages = get_pages(items)
    
    return templates.TemplateResponse(
        "videos/main.html", {
            "request": request, 
            "items": items, 
            'page_num': {'name': name, 'pages': pages, 'pagesize': settings._PAGESIZE},
            "is_token": is_token(token=request.cookies.get('access_token'),db=db),
            'etc_kwd': get_etc_keyword(db),
            },
        )

    
@router.get("/all_random/{page}", response_model=Page[VideoItem])
def view_all_random(
    request: Request, 
    db: Session=Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
    ):
    
    print(current_user.email)
    items = paginate(get_all_videos_random(db))
    name = ('all_random/', '?size=' + str(settings._PAGESIZE))
    pages = get_pages(items)
    
    return templates.TemplateResponse(
        "videos/main.html", {
            "request": request, 
            "items": items, 
            'page_num': {'name': name, 'pages': pages, 'pagesize': settings._PAGESIZE},
            "is_token": is_token(token=request.cookies.get('access_token'),db=db),
            'etc_kwd': get_etc_keyword(db),
            },
        )


@router.get("/choice_random/{page}", response_model=Page[VideoItem])
def view_choice_random(
    request: Request, 
    db: Session=Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
    ):
    
    items = paginate(get_all_choice_random(db))
    name = ('choice_random/', '?size=' + str(settings._PAGESIZE))
    pages = get_pages(items)
    
    return templates.TemplateResponse(
        "videos/main.html", {
            "request": request, 
            "items": items, 
            'page_num': {'name': name, 'pages': pages, 'pagesize': settings._PAGESIZE},
            "is_token": is_token(token=request.cookies.get('access_token'),db=db),
            'etc_kwd': get_etc_keyword(db),
            },
        )


@router.get("/nys_random/{page}", response_model=Page[VideoItem])
def view_nys_random(
    request: Request, 
    db: Session=Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
    ):
    
    items = paginate(get_all_nys_random(db))
    name = ('nys_random/', '?size=' + str(settings._PAGESIZE))
    pages = get_pages(items)
    
    return templates.TemplateResponse(
        "videos/main.html", {
            "request": request, 
            "items": items, 
            'page_num': {'name': name, 'pages': pages, 'pagesize': settings._PAGESIZE},
            "is_token": is_token(token=request.cookies.get('access_token'),db=db),
            'etc_kwd': get_etc_keyword(db),
            },
        )





@router.get("/search/{page}", response_model=Page[VideoItem])
def search(
    request: Request,
    db: Session=Depends(get_db),
    q: SearchVideos=Depends(),
    current_user: User = Depends(get_current_user_from_token),
    ):
    
    for i in ['star', 'keyword']:
        if (q.__dict__[i] == 0) | (q.__dict__[i] == ''):
            q.__dict__[i] = None
    
    result = search_videos(query=q.__dict__, db=db)
    
    if len(result) == 0:
        return RedirectResponse(url = "/videos")
    items = paginate(list(result))
    name = ('search/', '?size=' + str(settings._PAGESIZE) + '&' + str(request.url)[46:])
    pages = get_pages(items)
    
    return templates.TemplateResponse(
        "videos/main.html", {
            "request": request, 
            "items": items, 
            'page_num': {'name': name, 'pages': pages, 'pagesize': settings._PAGESIZE},
            "is_token": is_token(token=request.cookies.get('access_token'),db=db),
            'etc_kwd': get_etc_keyword(db),
            },
        )


@router.get("/update")
def update(
    request: Request,
    q: UpdateVideo=Depends(),
    db: Session=Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
    ):
    
    for i in ['star', 'ad_start', 'ad_finish', 'etc']:
        if (q.__dict__[i] == 0) | (q.__dict__[i] == '') | (q.__dict__[i] == ' '):
            q.__dict__[i] = None
    result = update_video(q.__dict__, db)
    q.__dict__.update(msg=result)
    print(result)
    return {"result": result}
    return templates.TemplateResponse(
        "videos/db/update_msg.html", {
            "request": request,
            'msg': result, 
            "is_token": is_token(token=request.cookies.get('access_token'),db=db),
            'etc_kwd': get_etc_keyword(db),
            }
        )


@router.get("/delete")
def delete(
    request: Request, 
    db: Session=Depends(get_db), 
    dbid: str = None,
    current_user: User = Depends(get_current_user_from_token),
    ):
    dbid = unquote(dbid)
    _db = del_video_dbid(dbid, db=db)
    _gif = del_gif(dbid)
    _webp = del_webp(dbid)
    _video = del_viedo(dbid)
    items = refix_video(db)
    # return {'del': ['_dbde', 'gifde', 'webp', 'video']}
    return {"del": [_db, _gif, _webp, _video]}
    return templates.TemplateResponse(
        'videos/refix/info.html', {
            'request': request, 
            'items': items, 
            'msgs': [_db, _gif, _webp, _video], 
            "is_token": is_token(token=request.cookies.get('access_token'),db=db),
            }
        )


@router.get('/strm')
async def read_root(request: Request, dbid: str):
    return templates.TemplateResponse(
        "videos/stream.html", {
            'request': request, 
            'dbid': dbid,
        }
    )


@router.get('/stream')
def get_video(request: Request, dbid: str):
    video_path = Path(settings.ROOT_DIR + dbid)
    return range_requests_response(
        request, file_path=video_path, content_type="video/mp4"
    )

    
    
    
# @router.get('/update_fetch')
# def update(
#     request: Request,
#     q: UpdateVideo=Depends(),
#     db: Session=Depends(get_db),
#     current_user: User = Depends(get_current_user_from_token),
# ):
#     for i in ['star', 'ad_start', 'ad_finish', 'etc']:
#         if (q.__dict__[i] == 0) | (q.__dict__[i] == '') | (q.__dict__[i] == ' '):
#             q.__dict__[i] = None
#     # result = update_video(q.__dict__, db)
#     result = 'successed'
#     # q.__dict__.update(msg=result)
#     print(q, '<=============')
#     print(result)
#     return result
#     return {'result': 'q'}@router.get('/update_fetch')
# def update(
#     request: Request,
#     q: UpdateVideo=Depends(),
#     db: Session=Depends(get_db),
#     current_user: User = Depends(get_current_user_from_token),
# ):
#     for i in ['star', 'ad_start', 'ad_finish', 'etc']:
#         if (q.__dict__[i] == 0) | (q.__dict__[i] == '') | (q.__dict__[i] == ' '):
#             q.__dict__[i] = None
#     # result = update_video(q.__dict__, db)
#     result = 'successed'
#     # q.__dict__.update(msg=result)
#     print(q, '<=============')
#     print(result)
#     return result
#     return {'result': 'q'}
    
        
# @router.websocket("/ws")
# async def websocket_endpoint(
#     websocket: WebSocket,
#     current_user: User = Depends(get_current_user_from_token),
#     ):
#     print(f"client connected : {websocket.client}")
#     await websocket.accept() # client의 websocket접속 허용
#     await websocket.send_text(f"Welcome client : {websocket.client}")
#     while True:
#         data = await websocket.receive_text()  # client 메시지 수신대기
#         print(f"message received : {data} from : {websocket.client}")
#         await websocket.send_text(f"Message text was: {data}") # client에 메시지 전달

# async def connect(msg):
#     with websockets.connect("ws://localhost:9080/videos/ws") as websocket:
#         while msg != None:
#             await websocket.send(msg)









add_pagination(router)