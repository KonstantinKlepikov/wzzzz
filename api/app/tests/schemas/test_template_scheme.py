import pytest
from pydantic.error_wrappers import ValidationError
from app.schemas import Template


class TestTemplateSchenes:
    """Test templates
    """

    def test_template_name_validation(self) -> None:
        """Test template name validation
        """
        data = Template.Config.schema_extra['example']

        data['name'] = 'to long name with so mutch different letters'
        with pytest.raises(
            ValidationError,
            match='limit_value=20'
            ):
            Template(**data)

        data['name'] = 'return (this==$Data)'
        with pytest.raises(
            ValidationError,
            match='string does not match regex'
            ):
            Template(**data)

        data['name'] = 'это не ascii'
        with pytest.raises(
            ValidationError,
            match='string does not match regex'
            ):
            Template(**data)
