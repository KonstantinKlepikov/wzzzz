import pytest
from pymongo.client_session import ClientSession
from app.crud import CRUDTemplate, CRUDUser
from app.schemas import Template, UserInDb


class TestCRUDTemplate:
    """Test crud vacancy
    """

    async def test_crud_tempalte_get(
        self,
        db: ClientSession,
        crud_template: CRUDTemplate,
        crud_user: CRUDUser,
            ) -> None:
        """Test crud template get
        """
        user = await crud_user.get(db, UserInDb.Config.schema_extra['example'])
        user_id = str(user['_id'])
        templ_name = Template.Config.schema_extra['example']['name']
        templates = await crud_template.get(db, {'name': templ_name, 'user': user_id})
        assert isinstance(templates, dict), 'wrong result type'
        assert templates['name'] == templ_name, 'wrong name'
        assert templates['user'] == user_id, 'wrong user id'

    async def test_crud_template_get_list_of_template_names(
        self,
        db: ClientSession,
        crud_template: CRUDTemplate,
        crud_user: CRUDUser,
            ) -> None:
        """Test crud template get names of templates
        """
        user = await crud_user.get(db, UserInDb.Config.schema_extra['example'])
        user_id = str(user['_id'])
        templates = await crud_template.get_names(db, {'user': user_id})
        assert isinstance(templates, list), 'wrong result type'
        assert len(templates) == 1, 'wrong len'
        assert templates[0]['name'] == Template.Config.schema_extra['example']['name'], \
            'wrong name'
