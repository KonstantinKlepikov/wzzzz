from typing import Any
from aiohttp import ClientSession
from aiogram import Bot
from app.schemas.scheme_errors import UserNotExistError, UserExistError
from app.config import settings


class QuerieMaker:
    """Api queries
    """
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def session(self) -> ClientSession:
        return await self.bot.get_session()

    async def get_user(self, user_id: int) -> dict[str, Any]:
        """Get user

        Args:
            user_id (int): user id

        Returns:
            dict[str, Any]: user from db
        """
        session = await self.bot.get_session()

        async with session.get(
            f'{settings.api_v1_str}/users/get_by_id',
            params={'user_id': user_id}
                ) as response:

            if response.status == 200:
                return await response.json()

            elif response.status == 404:
                raise UserNotExistError(user_id)

    async def create_user(self, user_id: int) -> None:
        """Create user

        Args:
            user_id (int): user id
        """
        session = await self.bot.get_session()

        async with session.post(
            f'{settings.api_v1_str}/users/create',
            params={'user_id': user_id}
                ) as response:

            if response.status == 201:
                return await response.json()

            elif response.status == 409:
                raise UserExistError(user_id)
