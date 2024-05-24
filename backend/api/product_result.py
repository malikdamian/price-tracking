from typing import Annotated

from fastapi import APIRouter, Body, Depends, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.database import ProductResult, get_db
from backend.schemas import (CreateProductResultModel,
                             GetProductResultModel,
                             PriceHistory)

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


@router.get(
    "/product-results",
    status_code=status.HTTP_200_OK,
    response_model=list[GetProductResultModel],
    summary="Get product results based on the search text",
)
def get_product_results(
    search_text: Annotated[str, Query(description="Search text to filter product results")],
    db: Annotated[Session, Depends(get_db)],
) -> list[GetProductResultModel]:
    """Retrieve a list of product results filtered by the search text."""
    query = (
        select(ProductResult)
        .where(ProductResult.search_text == search_text)
        .order_by(ProductResult.created.desc())
    )

    product_results = db.execute(query).scalars().all()

    product_dict: dict[str, GetProductResultModel] = {}
    for product in product_results:
        url = product.url
        if url not in product_dict:
            product_dict[url] = GetProductResultModel(
                name=product.name,
                url=product.url,
                source=product.source,
                image=product.image,
                created=product.created,
                price_history=[],
            )
        product_dict[url].price_history.append(
            PriceHistory(
                price=product.price,
                date=product.created,
            )
        )
    return list(product_dict.values())
