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

    class Config:
        schema_extra = {
            "example": {
                "detail": "Request parameters error",
                }
            }


class HttpError404(HttpErrorMessage):
    """404 Not Found
    """

    class Config:
        schema_extra = {
            "example": {
                "detail": "Resource not found",
            }
        }


class HttpError409(HttpErrorMessage):
    """409 Conflict
    """

    class Config:
        schema_extra = {
            "example": {
                "detail":
                    "Something wrong with client or server data",
                }
            }


class HttpError429(HttpErrorMessage):
    """429 To Many Requests
    """

    class Config:
        schema_extra = {
            "example": {
                "detail":
                    "To Many Requests",
                }
            }
