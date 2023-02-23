from socket import AF_INET
from typing import Optional, Any
from app.config import settings
import aiohttp


class SessionMaker:
    """This class realise aiohttp client session singleton pattern
    # TODO: test me
    """
    aiohttp_client: Optional[aiohttp.ClientSession] = None

    @classmethod
    def get_aiohttp_client(cls) -> aiohttp.ClientSession:
        """Get aiohttp client session

        Returns:
            ClientSession: client session object
        """

        if cls.aiohttp_client is None:
            timeout = aiohttp.ClientTimeout(total=settings.timeout_aiohttp)
            connector = aiohttp.TCPConnector(
                family=AF_INET,
                limit_per_host=settings.size_pool_http
                    )
            cls.aiohttp_client = aiohttp.ClientSession(
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
    async def simple_query(cls, url: str) -> Any:
        """Test query

        Args:
            url (str): test query

        Returns:
            Any: json response
        """
        client = cls.get_aiohttp_client()

        try:
            async with client.get(url) as response:
                if response.status != 200:
                    return {"ERROR OCCURED" + str(await response.text())}

                json_result = await response.json()

        except Exception as e:
            return {"ERROR": e}

        return json_result
