from fastapi import Request
from fastapi.responses import JSONResponse
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

async def category_not_found_handler(request: Request, exc: CategoryNotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})

async def category_exists_handler(request: Request, exc: CategoryAlreadyExistsError):
    return JSONResponse(status_code=409, content={"detail": str(exc)})

async def category_not_empty_handler(request: Request, exc: CategoryNotEmptyError):
    return JSONResponse(status_code=409, content={"detail": str(exc)})

async def brand_not_found_handler(request: Request, exc: BrandNotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})

async def brand_exists_handler(request: Request, exc: BrandAlreadyExistsError):
    return JSONResponse(status_code=409, content={"detail": str(exc)})

async def brand_not_empty_handler(request: Request, exc: BrandNotEmptyError):
    return JSONResponse(status_code=409, content={"detail": str(exc)})

async def product_not_found_handler(request: Request, exc: ProductNotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})

async def product_exists_handler(request: Request, exc: ProductAlreadyExistsError):
    return JSONResponse(status_code=409, content={"detail": str(exc)})

