from typing import Callable, Awaitable, Any
from aiogram import BaseMiddleware
from aiogram.types import Message
# from aiogram.fsm.storage.redis import RedisStorage
from app.middleware.api_queries import QuerieMaker


class SessionMiddleware(BaseMiddleware):
    """Aiohttp session middleware
    """

    def __init__(self, qm: QuerieMaker) -> None:
        self.qm = qm

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any]
    ) -> Any:
        """Get session for call to api middlewire
        """
        data['qm'] = self.qm
        return await handler(event, data)


# class ReddisMiddlewire(BaseMiddleware):
#     """Redis storage middleware
#     """

#     def __init__(self, storage: RedisStorage) -> None:
#         self.storage = storage

#     async def __call__(
#         self,
#         handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
#         event: Message,
#         data: dict[str, Any]
#     ) -> Any:
#         """Get redis storage
#         """
#         data['storage'] = self.storage
#         return await handler(event, data)
