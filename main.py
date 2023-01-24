from fastapi import FastAPI 
from fastapi.staticfiles import StaticFiles
from fastapi_pagination import add_pagination
from typing import Optional, List

from db.session import engine
from db.base import Base


from core.config import settings
from apis.base import api_router
from webapps.base import api_router as webapp_router

# from webapps.base import api_router as webapp_router
# from api.version1 import users
# from apis.version1 import chat

def create_tables():
    Base.metadata.create_all(bind=engine)


description = """
This is ya project 0.0.2 description
"""
# tags_metadata = [
#     {'name': 'videos', 'description': 'This is video router'},
# ]

def include_router(app):
    app.include_router(api_router)
    app.include_router(webapp_router)

# def add_middleware(app):
#     app.add_middleware(
#         CustomHeaderMiddleware,
#     )
    
def configure_static(app):
    app.mount("/static", StaticFiles(directory="static"), name="static")


def start_application():
    app = FastAPI(
        title = settings.PROJECT_TITLE,
        version = settings.PROJECT_VERSION,
        description = description,
        contact={"name": "KDS", "email": "kddddds@gmail.com"},
        max_size=3221225472,
    )
    create_tables()
    include_router(app)
    configure_static(app)
    # add_middleware(app)
    return app

app = start_application()

# app.router.redirect_slashes = False



