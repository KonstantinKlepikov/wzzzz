from typing import Any, Optional, TypeAlias
from aiohttp import ClientSession, ClientResponse
from aiogram import Bot
from app.schemas.scheme_errors import HttpError
from app.config import settings


Result: TypeAlias = dict[str, Any]


class QuerieMaker:
    """Api queries
    """
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

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

    # async def session(self) -> ClientSession:
    #     return await self.bot.get_session()

    async def get_user(self, user_id: int) -> Optional[Result]:
        """Get user

        Args:
            user_id (int): user id

        Returns:
            Optional[Result]: result of query
        """
        session = await self.bot.get_session()

        async with session.get(
            f'{settings.api_v1_str}/users/get_by_id',
            params={'user_id': user_id}
                ) as response:

            result = await self._get_response(200, response)
            return result

    async def create_user(self, user_id: int) -> Optional[Result]:
        """Create user

        Args:
            user_id (int): user id

        Returns:
            Optional[Result]: result of query
        """
        session = await self.bot.get_session()

        async with session.post(
            f'{settings.api_v1_str}/users/create',
            params={'user_id': user_id}
                ) as response:

            result = await self._get_response(201, response)
            return result

    async def get_templates_names(self, user_id: int) -> Optional[Result]:
        """Get names of templates

        Args:
            user_id (int): user id

        Returns:
            Optional[Result]: result of query
        """

        session = await self.bot.get_session()

        async with session.get(
            f'{settings.api_v1_str}/templates/get_names',
            params={'user_id': user_id}
                ) as response:

            result = await self._get_response(200, response)
            return result

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

        session = await self.bot.get_session()

        async with session.post(
            f'{settings.api_v1_str}/templates/create_empty',
            params={'user_id': user_id, 'template_name': template_name}
                ) as response:

            result = await self._get_response(201, response)
            return result
