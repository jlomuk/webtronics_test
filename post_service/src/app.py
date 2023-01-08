from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from api import root_router
from db.connection import create_tables

app = FastAPI(
    swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
    openapi_url="/api/v1/openapi.json"
)

app.include_router(root_router)


@app.on_event("startup")
async def startup():
    await create_tables()


openapi_schema = get_openapi(
    title="Post microservice",
    version="0.0.1",
    description="Post microservice",
    routes=app.routes,
)

app.openapi_schema = openapi_schema


