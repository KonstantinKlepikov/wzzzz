import pytest
import nest_asyncio
from pymongo.client_session import ClientSession
from pymongo.results import InsertOneResult
from app.crud.crud_vacancy import CRUDVacancies, CRUDVacanciesSimple
from app.schemas.scheme_vacancy import VacancyData


nest_asyncio.apply()


class TestCRUDVacancy:
    """Test crud vacancy
    """

    @pytest.mark.parametrize(
        'fixname', ['crud_vacancy_simple', 'crud_vacancy_deep']
            )
    async def test_crud_vacancy_create(
        self,
        db: ClientSession,
        fixname,
        request
            ) -> None:
        """Test vacancy creation
        """
        crud: CRUDVacancies = request.getfixturevalue(fixname)
        result = await crud.create(
            db,
            VacancyData(**VacancyData.Config.json_schema_extra["example"])
                )
        assert isinstance(result, InsertOneResult), 'wrong result'
        assert result.inserted_id, 'result hasnt _id'

    @pytest.mark.parametrize(
        'fixname', ['crud_vacancy_simple', 'crud_vacancy_deep']
            )
    async def test_crud_vacancy_get_by_vacancies_ids(
        self,
        db: ClientSession,
        fixname,
        request
            ) -> None:
        """Test crud vacancy get by id
        """
        crud: CRUDVacancies = request.getfixturevalue(fixname)
        result = await crud.get_many_by_v_ids(db, [54321, 654321])
        assert isinstance(result, list), 'wrong result'
        ids = [d['v_id'] for d in result]
        assert 654321 in ids, 'wrong id'
        assert 54321 in ids, 'wrong id'

    @pytest.mark.parametrize(
        'fixname', ['crud_vacancy_simple', 'crud_vacancy_deep']
            )
    async def test_crud_vacancy_get_notexisted_id(
        self,
        db: ClientSession,
        fixname,
        request
            ) -> None:
        """Test crud vacancy get notexisted id
        """
        crud: CRUDVacancies = request.getfixturevalue(fixname)
        result = await crud.get_many_notexisted_v_ids(db, {54321, 99999})
        assert isinstance(result, set), 'wrong result'
        assert 99999 in result, 'wrong not existed id'
        assert 54321 not in result, 'wrong existed id'

    @pytest.mark.skip("TODO: test me")
    @pytest.mark.parametrize(
        'fixname', ['crud_vacancy_simple', 'crud_vacancy_deep']
            )
    async def test_crud_vacancy_create_many(
        self,
        db: ClientSession,
        fixname,
        request
            ) -> None:
        """Test vacancy create many
        """
        crud = request.getfixturevalue(fixname)

    @pytest.mark.skip("TODO: test me")
    @pytest.mark.parametrize(
        'fixname', ['crud_vacancy_simple', 'crud_vacancy_deep']
            )
    async def test_crud_vaсancy_create_many_error_if_double(
        self,
        db: ClientSession,
        fixname,
        request
            ) -> None:
        """Test vacancy create many dublicate error
        """
        crud = request.getfixturevalue(fixname)


class TestCRUDVacancySimple:
    """Test crud vacancy for simple hhru api data
    """

    # TODO: test merging of data
    async def test_crud_vacancy_get_merged_by_vacancies_ids(
        self,
        db: ClientSession,
        crud_vacancy_simple: CRUDVacanciesSimple
            ) -> None:
        """Test crud vacancy simple get merged by ids
        """
        result = await crud_vacancy_simple.get_many_merged_by_v_ids(
            db, [54321, 654321]
                )
        assert isinstance(result, list), 'wrong result'
        ids = [d['v_id'] for d in result]
        assert 654321 in ids, 'wrong id'
        assert 54321 in ids, 'wrong id'



# this is for test crud basic
#     async def test_crud_vacancy_create(
#         self,
#         db: ClientSession,
#         crud_vacancy: CRUDVacancies
#             ) -> None:
#         """Test vacancy create
#         """
#         result = await crud_vacancy.create(db, VacancyResponseInDb(v_id=444555))
#         assert isinstance(result, InsertOneResult), 'wrong result'
#         assert result.inserted_id, 'result hasnt _id'
#         result = await db[Collections.VACANCIES.value].count_documents({})
#         assert result == 3, 'not added'

#     async def test_crud_vacancy_create_raise_error(
#         self,
#         db: ClientSession,
#         crud_vacancy: CRUDVacancies
#             ) -> None:
#         """Test vacancy raise error if vacancy id isnt unique
#         """
#         with pytest.raises(DuplicateKeyError) as e:
#             await crud_vacancy.create(db, VacancyResponseInDb(v_id=123456))
#             assert 'duplicate key error collection' in e.value.detail, 'wrong error'

#     async def test_crud_vacancy_replace(
#         self,
#         db: ClientSession,
#         crud_vacancy: CRUDVacancies
#             ) -> None:
#         """Test vacancy replace
#         """
#         result = await crud_vacancy.replace(
#             db,
#             {'v_id': 123456},
#             VacancyResponseInDb(v_id=999999)
#                 )
#         assert isinstance(result, UpdateResult), 'wrong result'
#         assert result.matched_count == 1, 'wrong matched count'
#         assert result.modified_count == 1, 'wrong updated count'
#         result = await db[Collections.VACANCIES.value].count_documents({})
#         assert result == 2, 'wrong replace'

#         result = await crud_vacancy.replace(
#             db,
#             {'v_id': 555555},
#             VacancyResponseInDb(v_id=999999)
#                 )
#         assert result.matched_count == 0, 'wrong matched count'
#         assert result.modified_count == 0, 'wrong updated count'

#         with pytest.raises(DuplicateKeyError) as e:
#             await crud_vacancy.replace(
#                 db,
#                 {'v_id': 999999},
#                 VacancyResponseInDb(v_id=654321)
#                     )
#             assert 'duplicate key error collection' in e.value.detail, 'wrong error'

#     async def test_crud_vacancy_delete(
#         self,
#         db: ClientSession,
#         crud_vacancy: CRUDVacancies
#             ) -> None:
#         """Test vacancy delete
#         """
#         result = await crud_vacancy.delete(db, {'v_id': 123456})
#         assert isinstance(result, DeleteResult), 'wrong result'
#         assert result.deleted_count == 1, 'wrong matched count'
#         result = await db[Collections.VACANCIES.value].count_documents({})
#         assert result == 1, 'not removed'

#         result = await crud_vacancy.delete(db, {'v_id': 555555})
#         assert result.deleted_count == 0, 'wrong matched count'
