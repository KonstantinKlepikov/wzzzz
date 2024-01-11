from app.config import settings
from app.crud.crud_base import CRUDBase
from app.schemas.constraint import Collections


class CRUDUser(CRUDBase):
    """Users crud
    """


users = CRUDUser(
    col_name=Collections.USERS.value,
    db_name=settings.DB_NAME,
        )
