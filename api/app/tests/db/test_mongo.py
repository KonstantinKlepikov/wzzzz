from typing import Generator
from app.db import get_client
from app.config import settings


class BdTestContext:
    def __init__(self, mongodb_url: str):
        self.client = get_client(mongodb_url)

    def __enter__(self):
        return self.client

    def __exit__(self, exc_type, exc_value, traceback):
        self.client.close()


class TestDB:
    """Db connections tests
    """

    def test_test_db_connection(self, db: Generator) -> None:
        """Test dev db is available
        """
        with BdTestContext(settings.TEST_MONGODB_URL) as cont:
            db = cont['test-db']
            assert db.name == 'test-db', 'wrong dev db'
