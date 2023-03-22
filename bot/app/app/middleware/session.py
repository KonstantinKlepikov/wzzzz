from typing import Callable, Awaitable, Any
from aiogram import BaseMiddleware
from aiogram.types import Message
from app.middleware.api_queries import QuerieMaker


class SessionMiddleware(BaseMiddleware):
    def __init__(self, qm) -> None:
        self.qm: QuerieMaker = qm

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
