from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from auth.schemas import UsersRegisterSchema
from auth.utils import AuthSystem

v1_routers = APIRouter()

auth = AuthSystem()


@v1_routers.post('/sign-up')
async def sign_up_user(data: Annotated[UsersRegisterSchema, Body()]):
    return await auth.register(data=data)


@v1_routers.post('/sign-in')
async def sign_in_user(
    form_data:  OAuth2PasswordRequestForm = Depends()
):
    return await auth.login(form_data=form_data)
