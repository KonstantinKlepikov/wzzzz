from pydantic import BaseModel


class HttpErrorMessage(BaseModel):
    """Http error
    """
    message: str

    class Config:
        schema_extra = {
            "example": {
                "detail": "Some information about error",
            }
        }


class HttpError400(HttpErrorMessage):
    """400 Bad Request
    """
    status_code: int = 400

    class Config:
        schema_extra = {
            "example": {
                "detail": "Reques parameters error",
                }
            }


class HttpError409(HttpErrorMessage):
    """409 Conflict
    """
    status_code: int = 409

    class Config:
        schema_extra = {
            "example": {
                "detail":
                    "Something wrong with client or server data",
                }
            }
