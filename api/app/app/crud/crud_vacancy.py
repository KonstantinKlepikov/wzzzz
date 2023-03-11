from app.config import settings
from app.crud import CRUDBase
from app.schemas import VacancyResponseInDb, Collections


class CRUDVacancies(CRUDBase[VacancyResponseInDb]):
    """Vacancies crud
    """


vacancies = CRUDVacancies(
    schema=VacancyResponseInDb,
    col_name=Collections.VACANCIES.value,
    db_name=settings.db_name,
        )
