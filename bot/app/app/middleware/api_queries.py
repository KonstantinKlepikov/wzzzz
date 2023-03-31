from typing import Any, Optional, TypeAlias
from aiohttp import ClientResponse
from aiogram import Bot
from app.schemas.scheme_errors import HttpError
from app.config import settings


Result: TypeAlias = dict[str, Any]


class QuerieMaker:
    """Api queries
    """
    def __init__(self, bot: Bot) -> None:
        self.session = bot.session

    async def _get_response(
        self,
        status: int,
        response: ClientResponse
            ) -> Optional[Result]:
        """Get response

        Args:
            status (int): status code for right response
            response (ClientResponse): response object

        Raises:
            HttpError: raises if status code wrong

        Returns:
            Optional[Result]: result
        """
        result = await response.json()
        if response.status == status:
            return result
        raise HttpError(str(result.get('detail')))

    async def get_user(self, user_id: int) -> Optional[Result]:
        """Get user

        Args:
            user_id (int): user id

        Returns:
            Optional[Result]: result of query
        """
        async with self.session as session:
            async with session._session.get(
                f'{settings.api_v1_str}/users/get_by_id',
                params={'user_id': user_id}
                    ) as response:
                return await self._get_response(200, response)

    async def create_user(self, user_id: int) -> Optional[Result]:
        """Create user

        Args:
            user_id (int): user id

        Returns:
            Optional[Result]: result of query
        """
        async with self.session as session:
            async with session._session.post(
                f'{settings.api_v1_str}/users/create',
                params={'user_id': user_id}
                    ) as response:
                return await self._get_response(201, response)

    async def get_templates_names(self, user_id: int) -> Optional[Result]:
        """Get names of templates

        Args:
            user_id (int): user id

        Returns:
            Optional[Result]: result of query
        """
        async with self.session as session:
            async with session._session.get(
                f'{settings.api_v1_str}/templates/get_names',
                params={'user_id': user_id}
                    ) as response:
                return await self._get_response(200, response)

    async def create_template(
        self,
        user_id: int,
        template_name: str
            ) -> Optional[Result]:
        """Create template

        Args:
            user_id (int): user id
            template_name (str): template name

        Returns:
            Optional[Result]: result of query
        """
        async with self.session as session:
            async with session._session.post(
                f'{settings.api_v1_str}/templates/create_empty',
                params={'user_id': user_id, 'template_name': template_name}
                    ) as response:
                return await self._get_response(201, response)

    async def get_template(
        self,
        user_id: int,
        template_name: str
            ) -> Optional[Result]:
        """Get template

        Args:
            user_id (int): user id
            template_name (str): template name

        Returns:
            Optional[Result]: result of query
        """
        async with self.session as session:
            async with session._session.get(
                f'{settings.api_v1_str}/templates/get',
                params={'user_id': user_id, 'template_name': template_name}
                    ) as response:
                return await self._get_response(200, response)

    async def delete_template(
        self,
        user_id: int,
        template_name: str
            ) -> Optional[Result]:
        """Delete template

        Args:
            user_id (int): user id
            template_name (str): template name

        Returns:
            Optional[Result]: result of query
        """
        async with self.session as session:
            async with session._session.delete(
                f'{settings.api_v1_str}/templates/delete',
                params={'user_id': user_id, 'template_name': template_name}
                    ) as response:
                return await self._get_response(200, response)