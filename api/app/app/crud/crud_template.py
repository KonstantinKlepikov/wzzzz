from typing import Any
from pymongo.client_session import ClientSession
from app.config import settings
from app.crud import CRUDBase
from app.schemas import TemplateConstraints, Collections


class CRUDTemplate(CRUDBase[TemplateConstraints]):
    """Templates crud
    """

    async def get_names(
        self,
        db: ClientSession,
        q: dict[str, Any],
        lenght: int = 100,
            ) -> list[dict[str, str]]:
        """Get names of template

        Args:
            db (ClientSession): session
            lenght (int, optional): maximum in result. Defaults to 100.

        Returns:
            list[dict[str, str]]: search result
        """
        data = db.client[self.db_name][self.col_name] \
            .find(q, projection=['name', ])
        return await data.to_list(length=lenght)


templates = CRUDTemplate(
    schema=TemplateConstraints,
    col_name=Collections.TEMPLATES.value,
    db_name=settings.db_name,
        )
