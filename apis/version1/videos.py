from fastapi import APIRouter, Request, Depends, status
from sqlalchemy.orm import Session
from fastapi_pagination import(
    LimitOffsetPage, add_pagination, paginate, Page, Params
)


from schemas.videos import VideoItem
from db.session import get_db
from db.repository.videos import get_all_videos
from apis.utils.videos.filename import cut_filename_len
# from db.repository.users import create_new_user

router =APIRouter()

@router.get("/all", response_model=Page[VideoItem])
def view_all(request: Request, db: Session=Depends(get_db)):
    videos = get_all_videos(db)
    return paginate(videos)


# @router.get('/cut_filename')
# def cut_filename(request: Request, db:Session=Depends(get_db)):
#     cut_filename_len(db)
#     return

 
add_pagination(router)