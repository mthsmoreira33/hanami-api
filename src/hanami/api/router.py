from fastapi import APIRouter
from .upload import router as upload_router
from .reports import router as reports_router

router = APIRouter()
router.include_router(upload_router)
router.include_router(reports_router)