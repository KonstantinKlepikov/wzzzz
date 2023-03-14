import pytest
from typing import Callable
from fastapi import HTTPException
from pymongo.client_session import ClientSession
from app.crud import CRUDUser, users
from app.schemas import UserInDb
from app.api.api_v1.endpoints import templ


class TestCheck:
    """Test check utilities
    """

    @pytest.fixture(scope="function")
    async def mock_user(
        self,
        crud_user: CRUDUser,
        monkeypatch,
            ) -> Callable:
        """Mock user data
        """
        async def mock_return(*args, **kwargs) -> Callable:
            return await crud_user.get(args[0], args[1])
        monkeypatch.setattr(users, "get", mock_return)

    async def test_check_user(
        self,
        mock_user: Callable,
        db: ClientSession,
            ) -> None:
        """Test check user
        """
        login = UserInDb.Config.schema_extra['example']['login']
        user = await templ.check_user(db, login)
        assert user['login'] == login, 'wrong return'


    async def test_check_user_raises_if_not_exist(
        self,
        mock_user: Callable,
        db: ClientSession,
            ) -> None:
        """Test check user
        """
        with pytest.raises(HTTPException) as e:
            await templ.check_user(db, 555)
            assert 'User 555 not exist' in e.value.detail, 'wrong error'
