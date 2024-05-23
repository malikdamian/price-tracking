from fastapi import APIRouter

from backend.api import product_result

router = APIRouter()

router.include_router(product_result.router)
