import redis.asyncio as redis
from app.config import settings


async def test_dev_redis_connection():
    """Test connection to redis db
    """
    r = redis.Redis(host=settings.REDIS_URL_DEV, port=6379, db=0)
    p = await r.ping()
    assert p, 'wrong ping'
    await r.close()