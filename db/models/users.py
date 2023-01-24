from email.policy import default
from db.base_class import Base
from sqlalchemy import Column, Integer, String, Boolean, Date, null, DateTime
from sqlalchemy.orm import relationship

class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    blogs = relationship('Blog', back_populates='creator')