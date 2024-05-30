from typing import Annotated

from fastapi import APIRouter, status, Query, Depends
from sqlalchemy.orm import Session

from backend.database import TrackedProducts, get_db

router = APIRouter(tags=["Tracked Product"])


@router.post(
    "/add-tracked-product",
    status_code=status.HTTP_201_CREATED,
    response_model=dict[str, str | int],
    summary="Add tracked product",
)
def add_tracked_product(
    name: Annotated[str, Query(description="Tracked product name")],
    db: Annotated[Session, Depends(get_db)],
) -> dict[str, str | int]:
    """Add tracked product to database."""
    tracked_product = TrackedProducts(name=name)
    db.add(tracked_product)
    db.commit()

    response: dict[str, str | int] = {
        "message": "Tracked product added successfully",
        "id": tracked_product.id,
    }
    return response
