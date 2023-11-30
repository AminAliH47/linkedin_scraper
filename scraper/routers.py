from fastapi import APIRouter
from scraper.api.v1.controllers import v1_routers

scraper_routers = APIRouter(prefix='/v1')
scraper_routers.include_router(v1_routers, prefix='/scrapers')
