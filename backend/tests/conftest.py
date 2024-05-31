from typing import Any, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from backend.database import Base, ProductResult, TrackedProducts, get_db
from backend.main import app

DATABASE_URL = "sqlite:///./test_db.db"
engine = create_engine(DATABASE_URL)

TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    except Exception as exc:
        db.rollback()
        raise exc
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client() -> Generator[TestClient, Any, None]:
    with TestClient(app) as client:
        yield client


@pytest.fixture
def session() -> Generator[Session, Any, Any]:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    except Exception as exc:
        db.rollback()
        raise exc
    finally:
        db.close()


@pytest.fixture
def submit_product(session: Session) -> ProductResult:
    product_result = ProductResult(
        name="Test-product",
        url="www.test.com",
        image="test.png",
        price=120.22,
        search_text="test-text",
        source="test-source",
    )
    session.add(product_result)
    session.commit()
    return product_result


@pytest.fixture
def tracked_product(session: Session) -> TrackedProducts:
    product = TrackedProducts(name="Test product")
    session.add(product)
    session.commit()
    return product
