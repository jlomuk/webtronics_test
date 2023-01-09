import asyncpg

from db.user_model import users
from sqlalchemy import insert, select
from fastapi.exceptions import HTTPException
from starlette import status
from schemas.user_schema import User
from databases import Database
from vendors.hunter_email import hunter_requestor


async def create_user(data: dict, database: Database):
    if not await hunter_requestor.verify_email(data['email']):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Предоставленная почта не является валидной/действующей')
    try:
        stmt = insert(users).returning(*users.c)
        result = await database.fetch_one(stmt, values=data)
        return result
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Такой пользователь уже существует')


async def get_user_by_email(email: str, database: Database) -> User:
    try:
        stmt = select(users).where(users.c.email == email)
        result = await database.fetch_one(stmt)
        return User(**result._mapping)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
