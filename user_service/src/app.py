from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from api import root_router
from db.user_model import get_db, init_db

app = FastAPI(
    swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
    openapi_url="/api/v1/openapi.json"
)

app.include_router(root_router)


@app.on_event("startup")
async def startup():
    init_db()
    db = get_db()
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    db = get_db()
    await db.disconnect()


openapi_schema = get_openapi(
    title="User service",
    version="0.0.1",
    description="User service",
    routes=app.routes,
)

app.openapi_schema = openapi_schema
