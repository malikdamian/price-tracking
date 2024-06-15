from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend import schemas
from backend.database import TrackedProducts, get_db

router = APIRouter(tags=["Tracked Product"])


@router.post(
    "/tracked-products",
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
    return {
        "message": "Tracked product added successfully",
        "id": tracked_product.id,
    }


@router.patch(
    "/tracked-products/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=dict[str, str],
    summary="Toggle tracked product",
)
def toggle_tracked_product(
    product_id: Annotated[int, Path(description="The ID of the product to be toggled")],
    db: Annotated[Session, Depends(get_db)],
) -> dict[str, str]:
    """Toggles the 'tracked' status of a product identified by its ID."""
    query = select(TrackedProducts).where(TrackedProducts.id == product_id)
    tracked_product = db.execute(query).scalar()

    if tracked_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tracked product not found."
        )

    tracked_product.tracked = not tracked_product.tracked
    db.commit()

    return {"message": "Tracked product toggled successfully"}


@router.get(
    "/tracked-products",
    status_code=status.HTTP_200_OK,
    response_model=list[schemas.GetTrackedProduct],
    summary="Get all tracked products",

)
def get_tracked_products(db: Annotated[Session, Depends(get_db)]) -> Sequence[TrackedProducts]:
    """Retrieve all tracked products from the database."""
    return db.execute(select(TrackedProducts)).scalars().all()
