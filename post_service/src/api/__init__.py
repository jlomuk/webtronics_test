from fastapi import APIRouter
from api.post_api import post_router

root_router = APIRouter(prefix='/api/v1')
root_router.include_router(post_router)