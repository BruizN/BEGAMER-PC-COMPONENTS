from fastapi import FastAPI
from app.modules.catalog.handlers import (
    category_exists_handler,
    category_not_found_handler,
    category_not_empty_handler,
    brand_exists_handler,
    brand_not_found_handler,
    brand_not_empty_handler,
    product_exists_handler,
    product_not_found_handler
)
from app.modules.catalog.exceptions import (
    CategoryNotFoundError, 
    CategoryAlreadyExistsError,
    CategoryNotEmptyError,
    BrandNotFoundError,
    BrandAlreadyExistsError,
    BrandNotEmptyError,
    ProductNotFoundError,
    ProductAlreadyExistsError
)
from app.modules.auth.router import router as auth_router
from app.modules.catalog.routers import catalog_router

app = FastAPI(
    title="BEGamer components", 
    version="0.1.0",
    swagger_ui_parameters={"persistAuthorization": True}
    )

app.add_exception_handler(CategoryNotFoundError, category_not_found_handler)
app.add_exception_handler(CategoryAlreadyExistsError, category_exists_handler)
app.add_exception_handler(CategoryNotEmptyError, category_not_empty_handler)
app.add_exception_handler(BrandNotFoundError, brand_not_found_handler)
app.add_exception_handler(BrandAlreadyExistsError, brand_exists_handler)
app.add_exception_handler(BrandNotEmptyError, brand_not_empty_handler)
app.add_exception_handler(ProductNotFoundError, product_not_found_handler)
app.add_exception_handler(ProductAlreadyExistsError, product_exists_handler)

@app.get("/health")
async def health():
    return {"status": "ok"}

#Routers por módulo
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(catalog_router)