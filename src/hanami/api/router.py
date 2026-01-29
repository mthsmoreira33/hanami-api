from fastapi import APIRouter
from .upload import router as upload_router
from .reports import router as reports_router
from .analytics import router as analytics_router
from .data import router as data_router

router = APIRouter()
router.include_router(upload_router)
router.include_router(reports_router)
router.include_router(analytics_router)
router.include_router(data_router)