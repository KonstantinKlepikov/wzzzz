from socket import AF_INET
from typing import Optional, Any
from aiohttp import ClientSession, ClientTimeout, TCPConnector
from fastapi import HTTPException
from app.config import settings


class SessionMaker:
    """This class realise aiohttp client session singleton pattern
    """
    aiohttp_client: Optional[ClientSession] = None

    @classmethod
    def get_aiohttp_client(cls) -> ClientSession:
        """Get aiohttp client session

        Returns:
            ClientSession: client session object
        """
        if cls.aiohttp_client is None:
            timeout = ClientTimeout(total=settings.timeout_aiohttp)
            connector = TCPConnector(
                family=AF_INET,
                limit_per_host=settings.size_pool_http
                    )
            cls.aiohttp_client = ClientSession(
                timeout=timeout,
                connector=connector
                    )

        return cls.aiohttp_client

    @classmethod
    async def close_aiohttp_client(cls) -> None:
        """Close aiohttp session
        """
        if cls.aiohttp_client:
            await cls.aiohttp_client.close()
            cls.aiohttp_client = None

    @classmethod
    async def vacancies_query(
        cls,
        url: str,
        params: Optional[dict[str, Any]] = None
            ) -> Any:

        client = cls.get_aiohttp_client()

        async with client.get(url, params=params) as response:
            if response.status == 400:
                raise HTTPException(
                    status_code=400,
                    detail="Reques parameters error"
                        )

            if response.status == 404:
                raise HTTPException(
                    status_code=404,
                    detail=f"Resource {url} not found"
                        )

            json_result = await response.text()

        return json_result
