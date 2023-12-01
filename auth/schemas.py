from pydantic import BaseModel, EmailStr
from tortoise.contrib.pydantic import pydantic_model_creator

from auth.models import Users


class UsersRegisterSchema(BaseModel):
    username: str
    email: EmailStr | None = None
    password: str


class UsersLoginSchema(BaseModel):
    username: str
    password: str


class TokenPayload(BaseModel):
    exp: int
    sub: str


UserPydantic = pydantic_model_creator(Users)
