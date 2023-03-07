from pymongo.client_session import ClientSession
from app.config import settings
from app.crud import CRUDBase
from app.schemas import VacancyConstraintsScheme
from app.schemas.constraint import Collections


class CRUDTemplate(CRUDBase[VacancyConstraintsScheme]):
    """Templates crud
    """

    async def get_names(
        self,
        db: ClientSession,
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
            .find(projection=['name', ])
        return await data.to_list(length=lenght)


template = CRUDTemplate(
    schema=VacancyConstraintsScheme,
    col_name=Collections.TEMPLATES.value,
    db_name=settings.db_name,
        )
