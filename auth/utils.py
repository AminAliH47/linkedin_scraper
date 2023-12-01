from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from pydantic import ValidationError

from auth.models import Users
from auth.schemas import TokenPayload, UserPydantic, UsersRegisterSchema
from auth import jwt_auth

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl='/v1/auth/sign-in',
    scheme_name='JWT'
)


class AuthSystem:
    async def register(self, data: UsersRegisterSchema):
        user = await Users.get_or_none(username=data.username)
        if user is not None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='User with this username already exist'
            )
        user = {
            'username': data.username,
            'email': data.email,
            'password': jwt_auth.get_hashed_password(data.password),
        }
        await Users.create(**user)
        return user

    async def login(self, form_data: OAuth2PasswordRequestForm):
        user = await Users.get_or_none(username=form_data.username)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Incorrect email or password'
            )

        hashed_pass = user.password
        if not jwt_auth.verify_password(form_data.password, hashed_pass):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Incorrect email or password'
            )

        return {
            'access_token': jwt_auth.create_access_token(user.username),
            'refresh_token': jwt_auth.create_refresh_token(user.username),
        }

    async def get_current_user(self, token: str = Depends(reuseable_oauth)):
        try:
            payload = jwt.decode(
                token, jwt_auth.SECRET_KEY, algorithms=[jwt_auth.ALGORITHM]
            )
            token_data = TokenPayload(**payload)

            if datetime.fromtimestamp(token_data.exp) < datetime.now():
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Token expired',
                    headers={'WWW-Authenticate': 'Bearer'},
                )

        except (jwt.JWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Could not validate credentials',
                headers={'WWW-Authenticate': 'Bearer'},
            )

        user = await Users.get_or_none(username=token_data.sub)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Could not find user',
            )

        return UserPydantic.model_validate(user)
