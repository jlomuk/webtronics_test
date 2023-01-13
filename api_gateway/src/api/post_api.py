from fastapi import APIRouter, Depends, Response, Query
from starlette import status

from helpers import request
from schemas import post, auth
from services.auth import auth_wrapper
from settings import settings

post_router = APIRouter(prefix='/post', tags=['post'], )


@post_router.get("/",
                 description='Получение списка всех постов пользователя',
                 responses={200: {"model": post.PostResponse}},
                 status_code=status.HTTP_200_OK)
async def get_list_post(offset: int = 0, limit: int = Query(default=10, lt=20), user=Depends(auth_wrapper)):
    url = settings.TASK_BACKEND_SERVICE.rstrip('/') + '/post/'
    result = await request.request(url, 'get', params={'limit': limit, 'offset': offset})
    return Response(content=result.content, status_code=result.status_code, media_type="application/json")


@post_router.get("/{post_id}",
                 description='Получение конкретного поста по id',
                 responses={200: {"model": post.PostResponse}},
                 status_code=status.HTTP_200_OK)
async def get_post(post_id: int, user=Depends(auth_wrapper)):
    url = f"{settings.TASK_BACKEND_SERVICE.rstrip('/')}/post/{post_id}"
    result = await request.request(url, 'get')
    return Response(content=result.content, status_code=result.status_code, media_type="application/json")


@post_router.post("/",
                  description='Добавление нового поста',
                  responses={201: {"model": post.PostCreateResponse}},
                  status_code=status.HTTP_201_CREATED)
async def add_post(new_post: post.CreatePostRequest, user: auth.User = Depends(auth_wrapper)):
    url = f"{settings.TASK_BACKEND_SERVICE.rstrip('/')}/post/"
    new_post.bind_user(user)
    result = await request.request(url, 'post', data=new_post.dict())
    return Response(content=result.content, status_code=result.status_code, media_type="application/json")


@post_router.patch("/{post_id}",
                   description='Обновление поста',
                   responses={200: {"model": post.PostResponse}},
                   status_code=status.HTTP_200_OK)
async def add_post(post_id: int, update_post: post.UpdatePostRequest, user: auth.User = Depends(auth_wrapper)):
    url = f"{settings.TASK_BACKEND_SERVICE.rstrip('/')}/post/{post_id}"
    update_post.bind_user(user)
    result = await request.request(url, 'patch', data=update_post.dict())
    return Response(content=result.content, status_code=result.status_code, media_type="application/json")


@post_router.delete("/{post_id}",
                    description='Удаление поста по id',
                    status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, user=Depends(auth_wrapper)):
    url = f"{settings.TASK_BACKEND_SERVICE.rstrip('/')}/post/{post_id}"
    result = await request.request(url, 'delete', params={'user_id': user.id})
    return Response(content=result.content, status_code=result.status_code, media_type="application/json")


@post_router.get("/{post_id}/like",
                 description='Лайк поста ',
                 responses={200: {"model": post.PostResponse}},
                 status_code=status.HTTP_200_OK)
async def like_post(post_id: int, user=Depends(auth_wrapper)):
    url = f"{settings.TASK_BACKEND_SERVICE.rstrip('/')}/post/{post_id}/like"
    result = await request.request(url, 'get', params={'user_id': user.id})
    return Response(content=result.content, status_code=result.status_code, media_type="application/json")


@post_router.get("/{post_id}/dislike",
                 description='Удаление поста по id',
                 responses={200: {"model": post.PostResponse}},
                 status_code=status.HTTP_200_OK)
async def dislike_post(post_id: int, user=Depends(auth_wrapper)):
    url = f"{settings.TASK_BACKEND_SERVICE.rstrip('/')}/post/{post_id}/dislike"
    result = await request.request(url, 'get', params={'user_id': user.id})
    return Response(content=result.content, status_code=result.status_code, media_type="application/json")
