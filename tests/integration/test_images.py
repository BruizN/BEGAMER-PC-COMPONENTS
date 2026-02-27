import pytest
from unittest.mock import patch
from io import BytesIO

# Intercepta la función upload_image_to_s3 para que no realice subidas a S3
@patch("app.modules.catalog.routers.images.upload_image_to_s3")
async def test_upload_product_image_ok(
    mock_upload,
    admin_client,
    product_factory
):
    mock_upload.return_value = "https://fake-bucket.s3.amazonaws.com/test-image.jpg"
    
    product = await product_factory(name="RTX 4090")
    
    # Simula una imagen
    fake_image = BytesIO(b"fake image data")

    files = {
        "file": ("foto.jpg", fake_image, "image/jpeg")
    }

    data = {
        "is_main": "true"
    }

    response = await admin_client.post(
        f"/catalog/products/{product.product_id}/images",
        files=files,
        data=data
    )

    assert response.status_code == 201
    response_data = response.json()
    
    assert response_data["image_url"] == "https://fake-bucket.s3.amazonaws.com/test-image.jpg"
    assert response_data["is_main"] == True
    assert response_data["product_id"] == str(product.product_id)

    mock_upload.assert_called_once()


async def test_upload_image_invalid_mime_type_rejected(
    admin_client, 
    product_factory
):
    prod = await product_factory(name="RX 7800 XT")
    
    # Simula un usuario malicioso que intenta subir un script de Python
    # pero le cambia el nombre a .jpg para engañar al sistema
    malicious_file = BytesIO(b"print('Me robe tu base de datos')")
    
    files = {
        "file": ("virus_oculto.jpg", malicious_file, "text/x-python") 
    }

    response = await admin_client.post(
        f"/catalog/products/{prod.product_id}/images",
        files=files
    )

    # El sistema debe detenerlo inmediatamente
    assert response.status_code == 415 # Unsupported Media Type
    assert response.json()["detail"] == "Only JPG, PNG and WEBP images are allowed"


async def test_deny_upload_image_too_large_rejected(
    admin_client, 
    product_factory
):
    prod = await product_factory(name="RX 7800 XT")
    
    # Simula una imagen demasiado grande
    too_large_file = BytesIO(b"a" * (1024 * 1024 * 10)) # 10MB
    
    files = {
        "file": ("foto.jpg", too_large_file, "image/jpeg")
    }

    response = await admin_client.post(
        f"/catalog/products/{prod.product_id}/images",
        files=files
    )

    # El sistema debe detenerlo inmediatamente
    assert response.status_code == 413