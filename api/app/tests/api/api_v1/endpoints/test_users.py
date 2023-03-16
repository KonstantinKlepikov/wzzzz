import pytest
from typing import Callable
from httpx import AsyncClient
from app.config import settings
from app.crud import users, CRUDUser
from app.schemas import UserInDb


class TestUsers:
    """Test users
    """

    @pytest.fixture(scope="function")
    async def mock_create(
        self,
        crud_user: CRUDUser,
        monkeypatch,
            ) -> None:
        """Mock create user
        """
        async def mock_return(*args, **kwargs) -> Callable:
            return await crud_user.create(*args)

        monkeypatch.setattr(users, "create", mock_return)

    @pytest.fixture(scope="function")
    async def mock_get(
        self,
        crud_user: CRUDUser,
        monkeypatch,
            ) -> None:
        """Mock get user
        """
        async def mock_return(*args, **kwargs) -> Callable:
            return await crud_user.get(*args)

        monkeypatch.setattr(users, "get", mock_return)

    async def test_post_users_create_returns_201(
        self,
        client: AsyncClient,
        mock_create: Callable,
            ) -> None:
        """Test create user
        """
        response = await client.post(
            f"{settings.api_v1_str}/users/create",
            params={'user_id': 45456897}
                )

        assert response.status_code == 201, f'{response.content=}'

    async def test_post_users_raises_if_doubles(
        self,
        client: AsyncClient,
        mock_create: Callable,
            ) -> None:
        """Test create double user rises error
        """
        user_id = UserInDb.Config.schema_extra['example']['user_id']
        response = await client.post(
            f"{settings.api_v1_str}/users/create",
            params={'user_id': user_id}
                )

        assert response.status_code == 409, f'{response.content=}'
        assert response.json()['detail'] == f'User {user_id} exist.', 'wrong error'

    async def test_get_users_by_id_200(
        self,
        client: AsyncClient,
        mock_get: Callable,
            ) -> None:
        """Test get user by id
        """
        response = await client.get(
            f"{settings.api_v1_str}/users/get_by_id",
            params={'user_id': 88005553535}
                )

        assert response.status_code == 200, f'{response.content=}'
        assert response.json()['user_id'] == 88005553535, 'wrong user id'

    async def test_get_users_raise_if_not_exist(
        self,
        client: AsyncClient,
        mock_get: Callable,
            ) -> None:
        """Test get user raises if not exist user
        """
        response = await client.get(
            f"{settings.api_v1_str}/users/get_by_id",
            params={'user_id': 555666}
                )

        assert response.status_code == 404, f'{response.content=}'
        assert response.json()['detail'] == f'User 555666 not exist.', \
            'wrong error'
