import os
from dotenv import load_dotenv
import redis.asyncio as redis
from typing import AsyncGenerator

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")


redis_pool = redis.ConnectionPool.from_url(
    REDIS_URL,
    decode_responses=True
)

async def get_redis_client() -> AsyncGenerator[redis.Redis, None]:
    """
    Dependencia de FastAPI para inyectar el cliente de Redis en los endpoints.
    """
    client = redis.Redis(connection_pool=redis_pool)
    try:
        yield client
    finally:
        await client.close()

async def test_redis_connection():
    """
    Función utilitaria para verificar que Redis está vivo al arrancar la API.
    """
    client = redis.Redis(connection_pool=redis_pool)
    try:
        ping = await client.ping()
        if ping:
            print("🟢 Connection to Redis successfully established.")
    except Exception as e:
        print(f"🔴 Error connecting to Redis: {e}")
    finally:
        await client.close()