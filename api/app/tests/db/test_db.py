from typing import Generator
from app.db import BdContext
from app.config import settings


class TestDB:
    """Db connections tests
    """

    async def test_dev_db_connection(self) -> None:
        """Test dev db is available
        """
        async with BdContext(settings.mongodb_url) as cont:
            db = cont[settings.db_name]
            assert db.name == 'dev-db', 'wrong dev db'

    async def test_test_db_connection(self, connection: Generator) -> None:
        """Test dev db is available
        """
        assert connection.name == 'test-db', 'wrong dev db'
