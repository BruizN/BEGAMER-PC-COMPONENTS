from fastapi import Request
from fastapi.responses import JSONResponse
from app.modules.catalog.exceptions import (
    CategoryNotFoundError, 
    CategoryAlreadyExistsError,
    CategoryNotEmptyError
)

async def category_not_found_handler(request: Request, exc: CategoryNotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})

async def category_exists_handler(request: Request, exc: CategoryAlreadyExistsError):
    return JSONResponse(status_code=409, content={"detail": str(exc)})

async def category_not_empty_handler(request: Request, exc: CategoryNotEmptyError):
    return JSONResponse(status_code=409, content={"detail": str(exc)})