from fastapi import APIRouter

from api.endpoints import facebook

api_router = APIRouter()
api_router.include_router(facebook.router, tags=["verify_token"])
