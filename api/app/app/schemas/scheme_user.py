from pydantic import BaseModel


class UserLogin(BaseModel):
    """User login
    """
    login: int

    class Config:

        schema_extra = {
                "example": {
                    'login': 88005553535
                        }
                    }


class UserInDb(UserLogin):
    """User and his templates
    """
