from app.config import settings
from app.crud.crud_base import CRUDBase
from app.schemas.scheme_user import UserInDb
from app.schemas.constraint import Collections


class CRUDUser(CRUDBase[UserInDb]):
    """Users crud
    """


users = CRUDUser(
    schema=UserInDb,
    col_name=Collections.USERS.value,
    db_name=settings.DB_NAME,
        )
