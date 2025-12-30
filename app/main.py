from fastapi import FastAPI
from app.modules.auth.router import router as auth_router

app = FastAPI(
    title="BEGamer components", 
    version="0.1.0",
    swagger_ui_parameters={"persistAuthorization": True}
    )


@app.get("/health")
async def health():
    return {"status": "ok"}

#Routers por módulo
app.include_router(auth_router, prefix="/auth", tags=["auth"])