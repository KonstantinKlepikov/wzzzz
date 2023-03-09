import pytest
from pymongo.client_session import ClientSession
from app.crud.crud_template import CRUDTemplate
from app.schemas import TemplateName


class TestCRUDTemplate:
    """Test crud vacancy
    """

    async def test_crud_template_get_list_of_template_names(
        self,
        db: ClientSession,
        crud_template: CRUDTemplate
            ) -> None:
        """Test crud template get names of templates
        """
        templates = await crud_template.get_names(db)
        assert isinstance(templates, list), 'wrong result type'
        assert len(templates) == 1, 'wrong len'
        assert templates[0]['name'] == TemplateName.Config.schema_extra['example']['name'], \
            'wrong name'
