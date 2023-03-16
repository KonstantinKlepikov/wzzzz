from typing import Optional, Any
from aiohttp import ClientSession
from aiogram import Bot
from app.config import settings


class QuerieMaker:
    """Api queries
    """
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def session(self) -> ClientSession:
        return await self.bot.get_session()

    async def get_user(self, user_id: int) -> dict[str, Any]:
        session = await self.bot.get_session()
        async with session.get(
            f'{settings.api_v1_str}/users/get_by_id',
            params={'user_id': user_id}
                ) as response:

            if response.status == 200:
                return await response.json()

            elif response.status == 404:
                return await response.json()
