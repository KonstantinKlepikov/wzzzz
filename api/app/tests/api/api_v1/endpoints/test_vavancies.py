from fastapi.testclient import TestClient
from app.config import settings


class TestVacancies:
    """Test vacancies
    """

    async def test_get_return_200(
        self,
        client: TestClient,
            ) -> None:
        """Test game data static return correct data
        """
        response = await client.get(f"{settings.api_v1_str}/test")

        assert response.status_code == 200, f'{response.content=}'