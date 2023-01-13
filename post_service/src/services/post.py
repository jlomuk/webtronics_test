from typing import NoReturn

from fastapi import Depends

from db.repository.post import PostCRUD
from db.repository.reaction import ReactionCRUD
from services.errors import NotFoundPost
from external.redis_cache.client import RedisCacheClient


class PostService:

    def __init__(self, post_crud=Depends(PostCRUD), reaction_crud=Depends(ReactionCRUD)):
        self.post_crud: PostCRUD = post_crud
        self.reaction_crud: ReactionCRUD = reaction_crud
        self.cache = RedisCacheClient()

    async def list(self) -> list[dict] | NoReturn:
        posts = await self.post_crud.list()
        if not posts:
            raise NotFoundPost

        result = []
        for post in posts:
            post_id = post['id']
            self.cache.pget(post_id)

        result_redis = await self.cache.execute_pipeline()

        missing_cache_post = []
        for index, reaction in enumerate(result_redis):
            post = dict(posts[index])
            if reaction:
                result.append(post | reaction)
            else:
                missing_cache_post.append(post['id'])

        if missing_cache_post:
            missed_cache_posts = await self.post_crud.retrieve_many_with_reaction(missing_cache_post)
            for post in missed_cache_posts:
                reaction = self.build_reaction(dict(post))
                self.cache.pset(post['id'], reaction)
                result.append(dict(post) | reaction)
            await self.cache.execute_pipeline()

        return result

    async def retrieve(self, pk: int) -> dict | NoReturn:
        data = await self.post_crud.retrieve(pk)
        if not data:
            raise NotFoundPost

        reaction = await self.cache.get(str(pk))
        if not reaction:
            data = await self.post_crud.retrieve_with_reaction(pk)
            reaction = self.build_reaction(data)
            await self.cache.set(str(pk), reaction)

        return data | reaction

    async def create(self, data: dict) -> dict:
        post = await self.post_crud.create(data)
        await self.reaction_crud.create({'post_id': post, 'user_id': data['user_id']})
        return {'post_id': post}

    async def delete(self, pk: int, user_id: int) -> NoReturn:
        data = await self.post_crud.delete(pk, user_id)
        if not data:
            raise NotFoundPost

    async def update(self, post_id: int, user_id: int, update_data: dict) -> dict | NoReturn:
        data = await self.post_crud.patch(post_id, user_id, update_data)
        if not data:
            raise NotFoundPost

        reaction = await self.cache.get(str(post_id))
        if not reaction:
            data = await self.post_crud.retrieve_with_reaction(post_id)
            reaction = self.build_reaction(data)
            await self.cache.set(str(post_id), reaction)

        return data | reaction

    async def like_post(self, post_id, user_id) -> dict | NoReturn:
        data = await self.reaction_crud.like(post_id, user_id)
        if not data:
            raise NotFoundPost

        reaction = self.build_reaction(data)
        await self.cache.set(str(post_id), reaction)
        return data | reaction

    async def dislike_post(self, post_id, user_id) -> dict | NoReturn:
        data = await self.reaction_crud.dislike(post_id, user_id)
        if not data:
            raise NotFoundPost

        reaction = self.build_reaction(data)
        await self.cache.set(str(post_id), reaction)
        return data | reaction

    @staticmethod
    def build_reaction(data: dict) -> dict:
        reaction = {'reaction': {'like': data.pop('like'), 'dislike': data.pop('dislike')}}
        return reaction
