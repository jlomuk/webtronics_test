from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from api import root_router

app = FastAPI(
    swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
    openapi_url="/api/v1/openapi.json"
)

app.include_router(root_router)


openapi_schema = get_openapi(
    title="Api gateway",
    version="0.0.1",
    description="Microservices api gateway",
    routes=app.routes,
)


app.openapi_schema = openapi_schema
