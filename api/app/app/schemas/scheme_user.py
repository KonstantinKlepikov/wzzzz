from pydantic import BaseModel


class UserId(BaseModel):
    """User id
    """
    user_id: int

    class Config:

        json_schema_extra = {
                "example": {
                    'user_id': 88005553535  # FIXME: string (???)
                        }
                    }


class User(UserId):
    """User
    """


class UserInDb(User):
    """User in bd
    """
