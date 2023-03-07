from app.config import settings
from app.crud import CRUDBase
from app.schemas import VacancyDb


class CRUDVacancies(CRUDBase[VacancyDb]):
    """Vacancies crud
    """


vacancies = CRUDVacancies(
    schema=VacancyDb,
    col_name='vacancies',
    db_name=settings.db_name,
        )
