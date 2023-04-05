from typing import TypeVar, Generic, Type, Optional, Any
from pydantic import BaseModel
from pymongo.client_session import ClientSession
from pymongo.results import InsertOneResult, UpdateResult, DeleteResult
from app.config import settings


SchemaDbType = TypeVar("SchemaDbType", bound=BaseModel)
SchemaReturnType = TypeVar("SchemaReturnType", bound=BaseModel)


class CRUDBase(Generic[SchemaDbType]):
    def __init__(
        self,
        schema: Type[SchemaReturnType],
        col_name: str,
        db_name: str = settings.db_name
            ):
        """
        CRUD object with default methods to Create,
        Read, Update, Delete (CRUD).
        """
        self.schema = schema
        self.col_name = col_name
        self.db_name = db_name

    async def get(
        self,
        db: ClientSession,
        q: dict[str, Any],
            ) -> Optional[dict[str, Any]]:
        """Get single document

        Args:
            db (ClientSession): session
            q: (dict[str, Any]): query filter

        Returns:
            Optional[dict[str, Any]]: search result
        """
        return await db.client[self.db_name][self.col_name].find_one(q)

    async def get_many(
        self,
        db: ClientSession,
        q: dict[str, Any],
        lenght: int = 100,
            ) -> list[dict[str, Any]]:
        """Get many documents

        Args:
            db (ClientSession): session
            q: (dict[str, Any]): query filter
            lenght (int, optional): maximum in result. Defaults to 100.

        Returns:
            list[dict[str, Any]]: search result
        """
        data = db.client[self.db_name][self.col_name].find(q)
        return await data.to_list(length=lenght)

    async def create(
        self,
        db: ClientSession,
        obj_in: SchemaDbType
            ) -> InsertOneResult:
        """Create document

        Args:
            db (ClientSession): session
            obj_in (SchemaDbType): scheme to creare

        Returns:
            InsertOneResult: result of creation
        """
        return await db.client[self.db_name][self.col_name] \
            .insert_one(obj_in.dict())

    async def replace(
        self,
        db: ClientSession,
        q: dict[str, Any],
        obj_in: SchemaDbType
            ) -> UpdateResult:
        """Replace one existed document

        Args:
            db (ClientSession): session
            q: (dict[str, Any]): query filter
            obj_in (SchemaDbType): scheme to update

        Returns:
            UpdateResult: result of update
        """
        return await db.client[self.db_name][self.col_name] \
            .replace_one(q, obj_in.dict())

    async def update(
        self,
        db: ClientSession,
        q: dict[str, Any],
        obj_in: dict[str, Any]
            ) -> UpdateResult:
        """Replace one existed document
        # TODO: test me and use me

        Args:
            db (ClientSession): session
            q: (dict[str, Any]): query filter
            obj_in (dict[str, Any]): data to update

        Returns:
            UpdateResult: result of update
        """
        return await db.client[self.db_name][self.col_name] \
            .replace_one(q, {'$set': obj_in})

    async def delete(
        self,
        db: ClientSession,
        q: dict[str, Any],
            ) -> DeleteResult:
        """Remove one document

        Args:
            db (ClientSession): session
            q: (dict[str, Any]): query filter

        Returns:
            DeleteResult: result of remove
        """
        return await db.client[self.db_name][self.col_name] \
            .delete_one(q)
