from fastapi import APIRouter
from auth.api.v1.controllers import v1_routers

auth_routers = APIRouter(prefix='/v1', tags=['Auth'])
auth_routers.include_router(v1_routers, prefix='/auth')
