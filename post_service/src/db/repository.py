from typing import TypeVar

from fastapi import Depends
from sqlalchemy import delete, insert, text, update, select
from sqlalchemy.engine import CursorResult
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.sql.schema import Table

from db.connection import get_engine
from db.models import post, reaction

TableType = TypeVar('TableType', bound=Table)


class PostCRUD:
    Post_table: TableType = post
    Reaction_table: TableType = reaction

    def __init__(self, conn: AsyncEngine = Depends(get_engine)):
        self.post_table: TableType = self.Post_table
        self.reaction_table: TableType = self.Reaction_table
        self.connection: AsyncEngine = conn

    async def list(self) -> dict:
        async with self.connection.begin() as conn:
            result: CursorResult = await conn.execute(text("""SELECT p.id, p.title, p.body,p.user_id, p.email, 
            p.created_date, count(*) FILTER (WHERE r."like" = true) AS like, 
            count(*) FILTER (WHERE r."like" = false) AS dislike
            
            FROM post p JOIN reaction r on p.id = r.post_id
            GROUP BY p.id, p.title, p.body, p.email, p.created_date
        """))
        return result.mappings().all()

    async def retrieve(self, pk: int) -> dict:
        stm = select(self.post_table).where(self.post_table.c.id == pk)
        async with self.connection.begin() as conn:
            result = await conn.execute(stm)
        return result.mappings().first()

    async def retrieve_with_reaction(self, pk: int) -> dict:
        async with self.connection.begin() as conn:
            result: CursorResult = await conn.execute(text("""SELECT p.id, p.title, p.body,p.user_id, p.email, 
            p.created_date, count(*) FILTER (WHERE r."like" = true) AS like, 
            count(*) FILTER (WHERE r."like" = false) AS dislike
            
            FROM post p JOIN reaction r on p.id = r.post_id
            WHERE p.id =:post_id 
            GROUP BY p.id, p.title, p.body, p.email, p.created_date""").bindparams(post_id=pk))
        return result.mappings().first()

    async def create(self, data: dict) -> int:
        statement = insert(self.post_table).returning(self.post_table.c.id, self.post_table.c.user_id)

        async with self.connection.begin() as conn:
            result: CursorResult = await conn.execute(statement, data)
            new_post = result.mappings().first()

        await self.create_reaction({'post_id': new_post.id, 'user_id': new_post.user_id})  # TODO: подумать!
        return new_post.id

    async def delete(self, pk: int, user_id: int) -> int:
        statement = delete(self.post_table).where(
            self.post_table.c.id == pk,
            self.post_table.c.user_id == user_id).returning(self.post_table.c.id)

        async with self.connection.begin() as conn:
            result = await conn.execute(statement)

        return result.mappings().first()

    async def patch(self, post_id: int, user_id: int, data: dict) -> dict:
        statement = update(self.post_table) \
            .where(self.post_table.c.id == post_id, self.post_table.c.user_id == user_id)

        async with self.connection.begin() as conn:
            res = await conn.execute(statement, data)

        return await self.retrieve_with_reaction(post_id)

    async def check_owner_post(self, post_id: int, user_id: int) -> bool:
        if not (exists_post:= await self.retrieve(post_id)):
            return False

        return exists_post['user_id'] != user_id

    async def get_reaction(self, post_id: int, user_id: int) -> dict:
        stm = select(self.reaction_table).where(self.reaction_table.c.post_id == post_id,
                                                self.reaction_table.c.user_id == user_id)
        async with self.connection.begin() as conn:
            result = await conn.execute(stm)
        return result.mappings().first()

    async def create_reaction(self, reaction_body: dict):
        stm = insert(self.reaction_table)

        async with self.connection.begin() as conn:
            await conn.execute(stm, reaction_body)

    async def update_reaction(self, exists_post: dict, reaction_type: bool):
        if (like := reaction_type) == exists_post['like']:
            like = None

        stm = update(self.reaction_table).where(self.reaction_table.c.id == exists_post['id'])
        async with self.connection.begin() as conn:
            await conn.execute(stm, {'like': like})

    async def action_reaction(self, post_id: int, user_id: int, reaction_type: bool):
        reaction_body = {'post_id': post_id, 'user_id': user_id, 'like': reaction_type}
        if await self.check_owner_post(post_id, user_id):
            exists_post = await self.get_reaction(post_id, user_id)
            if exists_post:
                await self.update_reaction(exists_post, reaction_type)
            else:
                await self.create_reaction(reaction_body)

        return await self.retrieve_with_reaction(post_id)

    async def like(self, post_id: int, user_id: int):
        return await self.action_reaction(post_id, user_id, reaction_type=True)

    async def dislike(self, post_id: int, user_id: int):
        return await self.action_reaction(post_id, user_id, reaction_type=False)
