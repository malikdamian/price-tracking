import uvicorn
from fastapi import FastAPI

from backend.api.router import router
from backend.config import settings
from backend.database import Base, engine

app = FastAPI(title=settings.APP_NAME, version=settings.VERSION)

app.include_router(router)

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=settings.RELOAD)
