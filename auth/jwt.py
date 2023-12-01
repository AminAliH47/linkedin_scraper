from datetime import datetime
from typing import Any
from passlib.context import CryptContext
from jose import jwt

from config.settings import JWT_AUTHENTICATION


class JWTAuth:
    def __init__(self):
        self.password_context = CryptContext(
            schemes=['bcrypt'],
            deprecated='auto'
        )
        self.ACCESS_TOKEN_EXPIRE_MINUTES = JWT_AUTHENTICATION['ACCESS_TOKEN_EXPIRE_MINUTES']
        self.REFRESH_TOKEN_EXPIRE_MINUTES = JWT_AUTHENTICATION['REFRESH_TOKEN_EXPIRE_MINUTES']
        self.ALGORITHM = JWT_AUTHENTICATION['ALGORITHM']
        self.SECRET_KEY = JWT_AUTHENTICATION['SECRET_KEY']

    def get_hashed_password(self, password: str) -> str:
        return self.password_context.hash(password)

    def verify_password(self, password: str, hashed_pass: str) -> bool:
        return self.password_context.verify(password, hashed_pass)

    def create_access_token(self, subject: str | Any) -> str:
        expires_delta = datetime.utcnow() + self.ACCESS_TOKEN_EXPIRE_MINUTES

        to_encode = {'exp': expires_delta, 'sub': str(subject)}
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, self.ALGORITHM)
        return encoded_jwt

    def create_refresh_token(self, subject: str | Any) -> str:
        expires_delta = datetime.utcnow() + self.REFRESH_TOKEN_EXPIRE_MINUTES

        to_encode = {'exp': expires_delta, 'sub': str(subject)}
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, self.ALGORITHM)
        return encoded_jwt


jwt_auth = JWTAuth()
