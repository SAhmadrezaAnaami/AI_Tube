from fastapi import APIRouter
from .register import router as register_router
from .login import router as login_router
from .search import router as search_router
from .video import router as video_router
from .getStatus import router as user_status

api_router = APIRouter()
api_router.include_router(register_router, tags=["Users"])
api_router.include_router(login_router, tags=["Users"])
api_router.include_router(search_router, tags=["search"])
api_router.include_router(video_router, tags=["video"])
api_router.include_router(user_status , tags=["Users"])
