from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db.models.users import User
from schemas import users as users_schemas # UserCreate, ShowUser
from db.session import get_db
from db.repository import users as users_crud
from core.security import get_current_user_from_token

router =APIRouter()


@router.post("/", response_model=users_schemas.ShowUser)
def create_user(
    user: users_schemas.UserCreate, 
    db: Session = Depends(get_db),
    current_user: users_schemas.User = Depends(get_current_user_from_token),
    ):
    user = users_crud.create_new_user(user, db)
    print(user)
    return user

@router.get("/list_users")
def get_users_list(db: Session = Depends(get_db),
                   current_user: users_schemas.User = Depends(get_current_user_from_token)):
    users = users_crud.get_all_user(db)
    users = [i for i in users]
    print(users)