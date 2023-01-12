from typing import TypeVar

from fastapi import Depends
from sqlalchemy import Table, update, insert, select
from sqlalchemy.ext.asyncio import AsyncEngine

from db.connection import get_engine
from db.models import reaction

from .post import PostCRUD

TableType = TypeVar('TableType', bound=Table)


class ReactionCRUD:
    REACTION_TABLE: TableType = reaction

    def __init__(self, post_crud: PostCRUD = Depends(PostCRUD), conn: AsyncEngine = Depends(get_engine)):
        self.reaction_table: TableType = self.REACTION_TABLE
        self.connection: AsyncEngine = conn
        self.post_crud = post_crud

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
        if await self.post_crud.check_owner_post(post_id, user_id):
            exists_post = await self.get_reaction(post_id, user_id)
            if exists_post:
                await self.update_reaction(exists_post, reaction_type)
            else:
                await self.create_reaction(reaction_body)

        return await self.post_crud.retrieve_with_reaction(post_id)

    async def like(self, post_id: int, user_id: int):
        return await self.action_reaction(post_id, user_id, reaction_type=True)

    async def dislike(self, post_id: int, user_id: int):
        return await self.action_reaction(post_id, user_id, reaction_type=False)
