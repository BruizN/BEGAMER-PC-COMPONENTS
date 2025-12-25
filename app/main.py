from fastapi import FastAPI


app = FastAPI(
    title="BEGamer components", 
    version="0.1.0",
    swagger_ui_parameters={"persistAuthorization": True}
    )


@app.get("/health")
async def health():
    return {"status": "ok"}