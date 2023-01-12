from typing import TypeVar, List

from fastapi import Depends
from sqlalchemy import delete, insert, text, update, select, bindparam
from sqlalchemy.engine import CursorResult
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.sql.schema import Table

from db.connection import get_engine
from db.models import post, reaction

TableType = TypeVar('TableType', bound=Table)


class PostCRUD:
    POST_TABLE: TableType = post

    def __init__(self, conn: AsyncEngine = Depends(get_engine)):
        self.post_table: TableType = self.POST_TABLE
        self.connection: AsyncEngine = conn

    async def list(self) -> dict:
        stm = select(self.post_table)

        async with self.connection.begin() as conn:
            result = await conn.execute(stm)
        return result.mappings().all()

    async def retrieve_many_with_reaction(self, posts_ids: List[int]) -> dict:
        stm = text("""SELECT p.id, p.title, p.body,p.user_id, p.email, 
            p.created_date, count(*) FILTER (WHERE r."like" = true) AS like, 
            count(*) FILTER (WHERE r."like" = false) AS dislike
            
            FROM post p JOIN reaction r on p.id = r.post_id
            WHERE p.id in :posts
            GROUP BY p.id, p.title, p.body, p.email, p.created_date""").bindparams(bindparam("posts", expanding=True))

        async with self.connection.begin() as conn:
            result: CursorResult = await conn.execute(stm, {'posts': posts_ids})
        return result.mappings().all()

    async def retrieve(self, pk: int) -> dict:
        stm = select(self.post_table).where(self.post_table.c.id == pk)

        async with self.connection.begin() as conn:
            result = await conn.execute(stm)

        result = result.mappings().first()
        return dict(result) if result else {}

    async def retrieve_with_reaction(self, pk: int) -> dict:
        async with self.connection.begin() as conn:
            result: CursorResult = await conn.execute(text("""SELECT p.id, p.title, p.body,p.user_id, p.email, 
            p.created_date, count(*) FILTER (WHERE r."like" = true) AS like, 
            count(*) FILTER (WHERE r."like" = false) AS dislike
            
            FROM post p JOIN reaction r on p.id = r.post_id
            WHERE p.id =:post_id 
            GROUP BY p.id, p.title, p.body, p.email, p.created_date""").bindparams(post_id=pk))

        result = result.mappings().first()
        return dict(result) if result else {}

    async def create(self, data: dict) -> int:
        stm = insert(self.post_table).returning(self.post_table.c.id, self.post_table.c.user_id)

        async with self.connection.begin() as conn:
            result: CursorResult = await conn.execute(stm, data)
            new_post = result.mappings().first()

        return new_post.id

    async def delete(self, pk: int, user_id: int) -> int:
        stm = delete(self.post_table).where(
            self.post_table.c.id == pk,
            self.post_table.c.user_id == user_id).returning(self.post_table.c.id)

        async with self.connection.begin() as conn:
            result = await conn.execute(stm)

        return result.mappings().first()

    async def patch(self, post_id: int, user_id: int, data: dict) -> dict:
        if not data:
            return await self.retrieve(post_id)

        stm = update(self.post_table) \
            .where(self.post_table.c.id == post_id, self.post_table.c.user_id == user_id).returning(
            *self.post_table.c)

        async with self.connection.begin() as conn:
            data = await conn.execute(stm, data)

        result = data.mappings().first()
        if not result:
            return {}
        return dict(result)

    async def check_owner_post(self, post_id: int, user_id: int) -> bool:
        if not (exists_post := await self.retrieve(post_id)):
            return False

        return exists_post['user_id'] != user_id
