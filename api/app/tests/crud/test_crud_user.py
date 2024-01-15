from pymongo.client_session import ClientSession
from app.crud.crud_user import CRUDUser
from app.schemas.scheme_user import UserInDb


class TestCRUDUser:
    """Test crud user
    """

    async def test_crud_user_get_user_by_user_id(
        self,
        db: ClientSession,
        crud_user: CRUDUser
            ) -> None:
        """Test crud vacancy get by id
        """
        data = UserInDb.Config.json_schema_extra['example']
        user = await crud_user.get(db, {'user_id': data['user_id']})
        assert isinstance(user, dict), 'wrong result type'
        assert user['user_id'] == data['user_id'], 'wrong data'
