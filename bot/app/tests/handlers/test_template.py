from app.handlers.template import parse_vacancy_ids


async def test_parse_vacancy_ids() -> None:
    """Test parse redis vacancy ids
    """
    ids = b'79312216 79304524 79308317 79292621'
    result = await parse_vacancy_ids(ids)
    assert isinstance(result, list), 'wrong result type'
    assert len(result) == 4, 'wrong result len'
    assert isinstance(result[0], int), 'wrong member type'
    assert result[0] == 79312216


async def test_parse_vacancy_ids_one() -> None:
    """Test parse redis vacancy ids if one id is given
    """
    ids = b'79312216'
    result = await parse_vacancy_ids(ids)
    assert isinstance(result, list), 'wrong result type'
    assert len(result) == 1, 'wrong result len'
    assert isinstance(result[0], int), 'wrong member type'
    assert result[0] == 79312216


async def test_parse_vacancy_ids_empty() -> None:
    """Test parse redis vacancy ids if empty is given
    """
    ids = b''
    result = await parse_vacancy_ids(ids)
    assert isinstance(result, list), 'wrong result type'
    assert len(result) == 0, 'wrong result len'
