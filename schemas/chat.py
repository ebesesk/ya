from pydantic import BaseModel, EmailStr

class RegisterValidator(BaseModel):
    username: str
