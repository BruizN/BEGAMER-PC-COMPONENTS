from fastapi import APIRouter
from . import categories, brands, products, variants

catalog_router = APIRouter(prefix="/catalog")
catalog_router.include_router(categories.router)
catalog_router.include_router(brands.router)
catalog_router.include_router(products.router)
catalog_router.include_router(variants.router)