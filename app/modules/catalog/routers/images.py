from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.core.aws import upload_image_to_s3, delete_image_from_s3
from app.core.dependencies import CurrentAdmin, SessionDep
from app.modules.catalog.models import ProductImage
from app.modules.catalog.schemas import ProductImageCreate, ProductImageRead, ProductImageUpdate
from app.modules.catalog import service as serv

router = APIRouter(tags=["Images"])

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_CONTENT_TYPES = ["image/jpeg", "image/png", "image/webp"]

@router.post(
    "/products/{product_id}/images",
    status_code=status.HTTP_201_CREATED,
    response_model=ProductImageRead,
    summary="Upload a generic image for a product."
)
async def upload_product_image(
    product_id: uuid.UUID,
    current_admin: CurrentAdmin,
    session: SessionDep,
    file: UploadFile = File(...),
    is_main: bool = Form(False)
):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Only JPG, PNG and WEBP images are allowed"
        )
    
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File size exceeds the 5MB limit"
        )
    
    await serv.get_product(session, product_id, only_active=False)
    image_url = upload_image_to_s3(file, "products")

    image_data = ProductImageCreate(
        product_id=product_id,
        image_url=image_url,
        is_main=is_main
    )

    return await serv.create_image(session, image_data)