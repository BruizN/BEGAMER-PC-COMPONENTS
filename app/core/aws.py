import boto3
from botocore.exceptions import ClientError
from fastapi import UploadFile, HTTPException
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")


# Inicializar el cliente S3
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)


def upload_image_to_s3(file: UploadFile, folder: str = "products") -> str:
    """
    Sube una imagen a S3 y devuelve la URL
    """
    try:
        # Generar un nombre unico para evitar colisiones
        file_extension = file.filename.split(".")[-1]
        unique_filename = f"{folder}/{uuid.uuid4().hex}.{file_extension}"

        # Subir el archivo
        s3_client.upload_fileobj(
            file.file,
            AWS_BUCKET_NAME,
            unique_filename,
            ExtraArgs={
                "ContentType": file.content_type
            }
        )

        # Construir y retornar la URL publica
        return f"https://{AWS_BUCKET_NAME}.s3.amazonaws.com/{unique_filename}"

    except ClientError as e:
        print(f"Error uploading to S3: {e}")
        raise HTTPException(status_code=503, detail="Connection error with the storage service")
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Unexpected error")

    
def delete_image_from_s3(image_url: str):
    """
    Elimina un archivo de AWS S3 a partir de su URL
    """
    try:
        # Extraer el 'Key' (ruta del archivo) desde la URL
            bucket_prefix = f"https://{AWS_BUCKET_NAME}.s3.amazonaws.com/"
            if image_url.startswith(bucket_prefix):
                object_key = image_url.replace(bucket_prefix, "")

                s3_client.delete_object(
                    Bucket=AWS_BUCKET_NAME,
                    Key=object_key
                )
             
    except ClientError as e:
        print(f"Error deleting from S3: {e}")