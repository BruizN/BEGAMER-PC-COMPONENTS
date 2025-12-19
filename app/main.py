from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.db import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan, 
    title="BEGamer components", 
    version="0.1.0",
    swagger_ui_parameters={"persistAuthorization": True})


@app.get("/health")
async def health():
    return {"status": "ok"}