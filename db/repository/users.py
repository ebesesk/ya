from sqlalchemy.orm import Session
from schemas.users import UserCreate
from db.models.users import User
from core.hashing import Hasher


def get_all_user(db: Session):
    return db.query(User).all()


def get_user(username: str, db: Session):
    user = db.query(User).filter(User.email == username).first()
    return user

def create_new_user(user: UserCreate, db: Session):
    user = User(
        username = user.username,
        email = user.email,
        hashed_password=Hasher.get_hash_password(user.password),
        is_active=True,
        is_superuser=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user