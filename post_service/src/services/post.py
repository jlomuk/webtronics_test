from typing import NoReturn

from fastapi import Depends

from db.repository import PostCRUD
from schemas.post import PostResponse
from services.errors import NotFoundPost


class PostService:

    def __init__(self, post_crud=Depends(PostCRUD)):
        self.post_crud: PostCRUD = post_crud

    async def list(self) -> list[PostResponse] | NoReturn:
        data = await self.post_crud.list()
        if not data:
            raise NotFoundPost
        return PostResponse.parse_obj(data)

    async def retrieve(self, pk: int) -> PostResponse | NoReturn:
        data = await self.post_crud.retrieve_with_reaction(pk)
        if not data:
            raise NotFoundPost
        return PostResponse.parse_obj(data)

    async def create(self, data: dict) -> dict:
        data = await self.post_crud.create(data)
        return {'post_id': data}

    async def delete(self, pk: int, user_id: int) -> NoReturn:
        data = await self.post_crud.delete(pk, user_id)
        if not data:
            raise NotFoundPost

    async def update(self, post_id: int, user_id: int, update_data: dict) -> PostResponse | NoReturn:
        data = await self.post_crud.patch(post_id, user_id, update_data)
        if not data:
            raise NotFoundPost
        return PostResponse.parse_obj(data)

    async def like_post(self, post_id, user_id) -> PostResponse:
        data = await self.post_crud.like(post_id, user_id)
        if not data:
            raise NotFoundPost
        return PostResponse.parse_obj(data)

    async def dislike_post(self, post_id, user_id) -> PostResponse:
        data = await self.post_crud.dislike(post_id, user_id)
        if not data:
            raise NotFoundPost
        return PostResponse.parse_obj(data)
