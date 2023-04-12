from app.config import settings
from app.crud import CRUDBase
from app.schemas import UserInDb, Collections


class CRUDUser(CRUDBase[UserInDb]):
    """Users crud
    """


users = CRUDUser(
    schema=UserInDb,
    col_name=Collections.USERS.value,
    db_name=settings.DB_NAME,
        )
