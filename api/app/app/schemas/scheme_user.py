from pydantic import BaseModel


class UserLogin(BaseModel):
    """User login
    """
    login: str

    class Config:

        schema_extra = {
                "example": {
                    'login': 'me'
                        }
                    }


class UserInDb(UserLogin):
    """User and his templates
    """
