import pytest
from typing import Callable
from httpx import AsyncClient
from app.config import settings
from app.crud import users, CRUDUser


class TestUsers:
    """Test users
    """

    @pytest.fixture(scope="function")
    async def mock_return(
        self,
        crud_user: CRUDUser,
        monkeypatch,
            ) -> None:
        """Mock user
        """
        async def mock_user(*args, **kwargs) -> Callable:
            return await crud_user.create(*args)

        monkeypatch.setattr(users, "create", mock_user)

    async def test_post_users_create_returns_201(
        self,
        client: AsyncClient,
        mock_return: Callable,
            ) -> None:
        """Test create user
        """
        response = await client.post(
            f"{settings.api_v1_str}/users/create",
            params={'login': 'new'}
                )

        assert response.status_code == 201, f'{response.content=}'

    async def test_post_users_raises_if_doubles(
        self,
        client: AsyncClient,
        mock_return: Callable,
            ) -> None:
        """Test create double user rises error
        """
        response = await client.post(
            f"{settings.api_v1_str}/users/create",
            params={'login': 'me'}
                )

        assert response.status_code == 409, f'{response.content=}'
        assert response.json()['detail'] == 'User me exist.', 'wrong error'
