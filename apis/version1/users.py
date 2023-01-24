from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db.models.users import User
from schemas.users import UserCreate, ShowUser
from db.session import get_db
from db.repository.users import create_new_user
from apis.version1.login import get_current_user_from_token

router =APIRouter()


@router.post("/", response_model=ShowUser)
def create_user(
    user: UserCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
    ):
    user = create_new_user(user, db)
    print(user)
    return user
