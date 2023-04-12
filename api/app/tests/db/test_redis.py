from app.db.init_redis import RedisConnection


class TestRedisDB:
    """Db connections tests
    """

    async def test_dev_redis_db_connection(self) -> None:
        """Test dev redis db is available
        """
        async with RedisConnection() as conn:
            ping = await conn.ping()
            assert ping is True, 'wrong ping'
