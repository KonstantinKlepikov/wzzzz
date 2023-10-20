import pytest
from typing import Callable
from httpx import AsyncClient
from fastapi import HTTPException
from app.config import settings
from app.crud import CRUDUser, users, templates, CRUDTemplate
from app.schemas import UserInDb, Template
from app.schemas.constraint import Area
from app.api.api_v1.endpoints import templ


class TestTemplates:
    """Test templates
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

    @pytest.fixture(scope="function")
    async def mock_check(
        self,
        crud_user: CRUDUser,
        monkeypatch,
            ) -> None:
        """Mock check user
        """
        async def mock_return(*args, **kwargs) -> Callable:
            user = await crud_user.get(args[0], {'user_id': args[1]})
            if user:
                return user
            raise HTTPException(
                status_code=404,
                detail=f"User {args[1]} not exist."
                    )
        monkeypatch.setattr(templ, "check_user", mock_return)

    @pytest.fixture(scope="function")
    async def mock_get(
        self,
        crud_template: CRUDTemplate,
        monkeypatch,
            ) -> Callable:
        """Mock template get
        """
        async def mock_return(*args, **kwargs) -> Callable:
            return await crud_template.get(args[0], args[1])
        monkeypatch.setattr(templates, "get", mock_return)

    @pytest.fixture(scope="function")
    async def mock_get_names(
        self,
        crud_template: CRUDTemplate,
        monkeypatch,
            ) -> Callable:
        """Mock templates names
        """
        async def mock_return(*args, **kwargs) -> Callable:
            return await crud_template.get_names(args[0], args[1])
        monkeypatch.setattr(templates, "get_names", mock_return)

    @pytest.fixture(scope="function")
    async def mock_delete(
        self,
        crud_template: CRUDTemplate,
        monkeypatch,
            ) -> Callable:
        """Mock template delete
        """
        async def mock_return(*args, **kwargs) -> Callable:
            return await crud_template.delete(args[0], args[1])
        monkeypatch.setattr(templates, "delete", mock_return)

    @pytest.fixture(scope="function")
    async def mock_replace(
        self,
        crud_template: CRUDTemplate,
        monkeypatch,
            ) -> Callable:
        """Mock template replace
        """
        async def mock_return(*args, **kwargs) -> Callable:
            return await crud_template.replace(args[0], args[1], args[2])
        monkeypatch.setattr(templates, "replace", mock_return)

    async def test_templates_create_returns_201(
        self,
        client: AsyncClient,
        mock_check: Callable,
            ) -> None:
        """Test create template
        """
        response = await client.post(
            f"{settings.API_V1}/templates/create_empty",
            params={
                'user_id': UserInDb.Config.json_schema_extra['example']['user_id'],
                'template_name': 'big_template'
                    }
                )
        assert response.status_code == 201, f'{response.content=}'

    async def test_templates_get_returns_200(
        self,
        client: AsyncClient,
        mock_check: Callable,
        mock_get: Callable
            ) -> None:
        """Test get template
        """
        templ_n = Template.Config.json_schema_extra['example']['name']
        response = await client.get(
            f"{settings.API_V1}/templates/get",
            params={
                'user_id': UserInDb.Config.json_schema_extra['example']['user_id'],
                'template_name': templ_n
                    }
                )
        assert response.status_code == 200, f'{response.content=}'
        assert response.json()['name'] == templ_n, 'wrong template'

    async def test_templates_get_raises_404(
        self,
        client: AsyncClient,
        mock_check: Callable,
        mock_get: Callable
            ) -> None:
        """Test get not existed template
        """
        response = await client.get(
            f"{settings.API_V1}/templates/get",
            params={
                'user_id': UserInDb.Config.json_schema_extra['example']['user_id'],
                'template_name': 'not_existed'
                    }
                )
        assert response.status_code == 404, f'{response.content=}'
        assert response.json()['detail'] == 'Template not found.', 'wrong error'

    async def test_get_list_of_templates_returns_200(
        self,
        client: AsyncClient,
        mock_check: Callable,
        mock_get_names: Callable
            ) -> None:
        """Test get list of templates
        """
        templ_n = Template.Config.json_schema_extra['example']['name']
        response = await client.get(
            f"{settings.API_V1}/templates/get_names",
            params={
                'user_id': UserInDb.Config.json_schema_extra['example']['user_id'],
                    }
                )
        assert response.status_code == 200, f'{response.content=}'
        assert len(response.json()['names']) == 1, 'wrong returned len'
        assert response.json()['names'][0]['name'] == templ_n, \
            'wrong templates names'

    async def test_delete_template_returns_200(
        self,
        client: AsyncClient,
        mock_check: Callable,
        mock_delete: Callable
            ) -> None:
        """Test delete template
        """
        templ_n = Template.Config.json_schema_extra['example']['name']
        response = await client.delete(
            f"{settings.API_V1}/templates/delete",
            params={
                'user_id': UserInDb.Config.json_schema_extra['example']['user_id'],
                'template_name': templ_n
                    }
                )
        assert response.status_code == 200, f'{response.content=}'

    async def test_delete_template_raises_404(
        self,
        client: AsyncClient,
        mock_check: Callable,
        mock_delete: Callable
            ) -> None:
        """Test delete not existed template
        """
        response = await client.delete(
            f"{settings.API_V1}/templates/delete",
            params={
                'user_id': UserInDb.Config.json_schema_extra['example']['user_id'],
                'template_name': 'not_existed'
                    }
                )
        assert response.status_code == 404, f'{response.content=}'
        assert response.json()['detail'] == 'Template not found.', 'wrong error'

    async def test_replace_template_returns_200(
        self,
        client: AsyncClient,
        mock_check: Callable,
        mock_replace: Callable
            ) -> None:
        """Test replace template
        """
        templ = Template.Config.json_schema_extra['example']
        templ['area'] = [Area.KAZAKHSTAN, ]
        templ = Template(**templ).json()
        response = await client.patch(
            f"{settings.API_V1}/templates/replace",
            params={
                'user_id': UserInDb.Config.json_schema_extra['example']['user_id'],
                       },
            data=templ
                )
        assert response.status_code == 200, f'{response.content=}'
