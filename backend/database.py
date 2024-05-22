from datetime import datetime
from typing import Generator

from sqlalchemy import DECIMAL, DateTime, String, create_engine, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from backend.config import settings

engine = create_engine(settings.DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    except Exception as exc:
        db.rollback()
        raise exc
    finally:
        db.close()


class Base(DeclarativeBase):
    pass


class ProductResult(Base):
    __tablename__ = "product_result"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(512))
    image: Mapped[str] = mapped_column(String(512))
    url: Mapped[str] = mapped_column(String(512))
    price: Mapped[float] = mapped_column(DECIMAL)
    search_text: Mapped[str] = mapped_column(String(256))
    source: Mapped[str] = mapped_column(String(256))
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class TrackedProducts(Base):
    __tablename__ = "tracked_product"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(512))
    tracked: Mapped[bool] = mapped_column(default=True)
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
