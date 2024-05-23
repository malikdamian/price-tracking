from typing import Annotated

from fastapi import APIRouter, Body, Depends, status
from sqlalchemy.orm import Session

from backend.database import ProductResult, get_db
from backend.schemas import CreateProductResultModel

router = APIRouter(tags=["Product result"])


@router.post(
    "/product-results",
    status_code=status.HTTP_201_CREATED,
    response_model=dict[str, str],
    summary="Submit new product results",
)
def submit_result(
    product: Annotated[CreateProductResultModel, Body(description="Product data to be submitted")],
    db: Annotated[Session, Depends(get_db)],
) -> dict[str, str]:
    """Submit new product results to the database."""
    product_results: list[ProductResult] = []
    for result in product.results:
        product_result = ProductResult(
            name=result.name,
            url=result.url,
            image=result.image,
            price=result.price,
            search_text=product.search_text,
            source=product.source,
        )
        product_results.append(product_result)

    db.add_all(product_results)
    db.commit()
    return {"message": "Received data successfully"}
