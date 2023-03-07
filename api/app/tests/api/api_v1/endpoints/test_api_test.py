from fastapi.testclient import TestClient
from app.config import settings


class TestApiTest:
    """Test api
    """

    def test_get_db_name_200(
        self,
        client: TestClient,
            ) -> None:
        """Test game data static return correct data
        """
        response = client.get(f"{settings.api_v1_str}/test/get_db_name")

        assert response.status_code == 200, f'{response.content=}'
        assert response.json()['name'] == settings.db_name, 'wrong db name'