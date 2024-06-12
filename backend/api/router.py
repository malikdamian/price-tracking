from fastapi import APIRouter

from backend.api import product_result, tracked_product

router = APIRouter()

router.include_router(product_result.router)
router.include_router(tracked_product.router)