from re import template
from fastapi import APIRouter, Request, Response, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from core.security import (
    get_authorization_scheme_param, get_current_user_from_token, oauth2_scheme,
    authenticate_user, create_access_token
)
from db.session import get_db
from webapps.forms.login_form import LoginForm
from apis.version1.login import login_for_access_token


router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="templates")
router.mount("/static", StaticFiles(directory="static"), name="static")


@router.get("/")
def login(request: Request,
          msg: str = None,
          db: Session=Depends(get_db)):
    try:
        authorization = request.cookies.get("access_token")
        scheme, param = get_authorization_scheme_param(authorization)
        user = get_current_user_from_token(token=param, db=db)
        print(user)
        return RedirectResponse(url="/videos")
    except HTTPException:
        return templates.TemplateResponse("auth/login.html", {"request": request}) 
    
@router.post("/")
async def login(response:Response, request:Request, db:Session=Depends(get_db)):
    form = await request.form()
    username = form.get("username")
    password = form.get("password")
    errors = []
    try:
        user = authenticate_user(username=username, password=password, db=db)
        if isinstance(user,dict):
            errors.append(user['errors'])
            return templates.TemplateResponse("auth/login.html", {"request":request, "errors":errors})
        access_token = create_access_token(data={"sub":username})
        response = RedirectResponse(url="/", status_code=302)
        response.set_cookie(key="access_token",
                            value=f"Bearer {access_token}",
                            httponly=True)
        return response
    except HTTPException:
        errors.append("Incorrect Username or password")
        return templates.TemplateResponse("auth/login.html", {"request": request, "errors":errors}) 
    # form = LoginForm(request)
    # await form.load_data()
    # if await form.is_valid():
    #     try:
    #         form.__dict__.update(msg="Login Successful")
    #         response = templates.TemplateResponse("auth/login.html", form.__dict__)
    #         login_for_access_token(
    #             response=response, form_data=form, db=db
    #         )
    #         return response
    #     except HTTPException:
    #         form.__dict__.update(msg="")
    #         form.__dict__.get("errors").append("Incorrect Username or password")
    #         return templates.TemplateResponse("auth/login.html", form.__dict__)
    # return templates.TemplateResponse("auth/login.html", form.__dict__)

@router.get("/logout")
def logout(request: Request, response: Response, token: str = Depends(oauth2_scheme)):
    response = RedirectResponse(url="/")
    response.delete_cookie("access_token")
    return response
    