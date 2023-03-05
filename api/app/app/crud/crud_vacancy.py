from typing import TypeVar, Generic, Type, Optional, Any
from pydantic import BaseModel
from pymongo.client_session import ClientSession
from bson.objectid import ObjectId
from app.config import settings


SchemaType = TypeVar("SchemaType", bound=BaseModel)


class CRUDBase(Generic[SchemaType]):
    def __init__(
        self,
        schema: Type[SchemaType],
        col_name: str,
        db_name: str = settings.db_name
            ):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        """
        self.schema = schema
        self.col_name = col_name
        self.db_name = db_name

    async def get(
        self,
        db: ClientSession,
        field_name: str,
        field_value: Any
            ) -> Optional[SchemaType]:
        data = await db.client[self.db_name][self.col_name] \
            .find_one({field_name: field_value})
        return self.schema(**data)

    # def get_multi(
    #     self, db: Session, *, skip: int = 0, limit: int = 100
    # ) -> List[ModelType]:
    #     return db.query(self.model).offset(skip).limit(limit).all()

    # def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
    #     obj_in_data = jsonable_encoder(obj_in)
    #     db_obj = self.model(**obj_in_data)  # type: ignore
    #     db.add(db_obj)
    #     db.commit()
    #     db.refresh(db_obj)
    #     return db_obj

    # def update(
    #     self,
    #     db: Session,
    #     *,
    #     db_obj: ModelType,
    #     obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    # ) -> ModelType:
    #     obj_data = jsonable_encoder(db_obj)
    #     if isinstance(obj_in, dict):
    #         update_data = obj_in
    #     else:
    #         update_data = obj_in.dict(exclude_unset=True)
    #     for field in obj_data:
    #         if field in update_data:
    #             setattr(db_obj, field, update_data[field])
    #     db.add(db_obj)
    #     db.commit()
    #     db.refresh(db_obj)
    #     return db_obj

    # def remove(self, db: Session, *, id: int) -> ModelType:
    #     obj = db.query(self.model).get(id)
    #     db.delete(obj)
    #     db.commit()
    #     return obj
