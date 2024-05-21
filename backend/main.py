import uvicorn
from fastapi import FastAPI

from backend.config import settings

app = FastAPI(title=settings.APP_NAME, version=settings.VERSION)

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=settings.RELOAD)
