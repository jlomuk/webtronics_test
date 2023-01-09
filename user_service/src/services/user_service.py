import asyncpg
from databases import Database
from fastapi.exceptions import HTTPException
from sqlalchemy import insert, select
from starlette import status

from db.user_model import users
from schemas.user_schema import User
from vendors.hunter_email import HunterRequester


async def create_user(data: dict, database: Database, hunter_checker: HunterRequester):
    transaction = await database.transaction()
    try:
        stmt = insert(users).returning(*users.c)
        result = await database.fetch_one(stmt, values=data)

        if not await hunter_checker.verify_email(data['email']):
            await transaction.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Предоставленная почта не является валидной/действующей')

        await transaction.commit()
        return result

    except asyncpg.exceptions.UniqueViolationError:
        await transaction.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Такой пользователь уже существует')


async def get_user_by_email(email: str, database: Database) -> User:
    try:
        stmt = select(users).where(users.c.email == email)
        result = await database.fetch_one(stmt)
        return User(**result._mapping)
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
