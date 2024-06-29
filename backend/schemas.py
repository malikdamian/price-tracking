from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CustomModel(BaseModel):
    model_config = ConfigDict()


class Result(CustomModel):
    name: str
    url: str
    image: str
    price: float


class CreateProductResultModel(CustomModel):
    search_text: str
    source: str
    results: list[Result]


class PriceHistory(CustomModel):
    price: float
    date: datetime


class GetProductResultModel(CustomModel):
    name: str
    url: str
    image: str
    source: str
    created: datetime
    price_history: list[PriceHistory]


class GetAllProductResultModel(CustomModel):
    id: int
    name: str
    url: str
    price: float
    image: str
    source: str
    search_text: str
    created: datetime


class GetTrackedProduct(CustomModel):
    id: int
    name: str
    tracked: bool
    created: datetime
