import pytest
from pydantic import ValidationError
from app.schemas.scheme_templates import Template


class TestTemplateSchenes:
    """Test templates
    """

    def test_template_name_validation(self) -> None:
        """Test template name validation
        """
        data = Template.Config.json_schema_extra['example']

        data['name'] = 'to long name with so mutch different letters'
        with pytest.raises(
            ValidationError,
            match='string_too_long'
                ):
            Template(**data)

        data['name'] = 'return (this==$Data)'
        with pytest.raises(
            ValidationError,
            match='string_pattern_mismatch'
                ):
            Template(**data)

        data['name'] = 'это не ascii'
        with pytest.raises(
            ValidationError,
            match='string_pattern_mismatch'
                ):
            Template(**data)
