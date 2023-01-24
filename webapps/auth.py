from re import template
from fastapi import APIRouter, Request, Response, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from apis.version1.login import oauth2_scheme
from db.session import get_db
from webapps.forms.login_form import LoginForm
from apis.version1.login import login_for_access_token


router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="templates")
router.mount("/static", StaticFiles(directory="static"), name="static")


@router.get("/login")
def login(request: Request, msg: str = None):
    return templates.TemplateResponse(
        "auth/login.html", {"request": request, "msg": msg, "is_token": False}
    )
    
    
@router.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):
    form = LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            form.__dict__.update(msg="Login Successful")
            response = templates.TemplateResponse("auth/login.html", form.__dict__)
            login_for_access_token(
                response=response, form_data=form, db=db
            )
            return response
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Incorrect Username or password")
            return templates.TemplateResponse("auth/login.html", form.__dict__)
    return templates.TemplateResponse("auth/login.html", form.__dict__)

@router.get("/logout")
def logout(request: Request, response: Response, token: str = Depends(oauth2_scheme)):
    response = RedirectResponse(url="/videos")
    response.delete_cookie("access_token")
    return response
    