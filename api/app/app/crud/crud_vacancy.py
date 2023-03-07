from app.config import settings
from app.crud import CRUDBase
from app.schemas import VacancyResponseSchemeDb
from app.schemas.constraint import Collections


class CRUDVacancies(CRUDBase[VacancyResponseSchemeDb]):
    """Vacancies crud
    """


vacancies = CRUDVacancies(
    schema=VacancyResponseSchemeDb,
    col_name=Collections.VACANCIES.value,
    db_name=settings.db_name,
        )
