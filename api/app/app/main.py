from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings


app = FastAPI(
    title=settings.title,
    openapi_url=f"{settings.api_v1_str}/openapi.json",
    description=settings.descriprion,
    version=settings.version,
    openapi_tags=settings.openapi_tags,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}
        )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}
