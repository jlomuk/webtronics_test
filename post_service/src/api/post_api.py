from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from starlette import status

from schemas import post
from services.errors import NotFoundPost
from services.post import PostService
from settings import logger

post_router = APIRouter(prefix='/post', tags=['post'])


@post_router.get("/",
                 description='Получение списка всех постов пользователя',
                 response_model=list[post.PostResponse],
                 status_code=status.HTTP_200_OK)
async def get_list_post(post_service=Depends(PostService)):
    try:
        result = await post_service.list()
    except NotFoundPost:
        return []
    except ValidationError as e:
        logger.warning(e.errors())
        raise HTTPException(status_code=422, detail=e.errors())
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail='Неизвестная ошибка')
    else:
        return result


@post_router.get("/{post_id}",
                 description='Получение конкретного поста по id',
                 response_model=post.PostResponse,
                 status_code=status.HTTP_200_OK)
async def get_post(post_id: int, post_service: PostService = Depends(PostService)):
    try:
        result = await post_service.retrieve(pk=post_id)
    except ValidationError as e:
        logger.warning(e.errors())
        raise HTTPException(status_code=422, detail=e.errors())
    except NotFoundPost:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Пост не найден')
    except Exception as e:
        logger.warning(e)
        raise HTTPException(status_code=500, detail='Неизвестная ошибка')
    else:
        return result


@post_router.patch("/{post_id}",
                   description='Обновление конкретного поста по id',
                   response_model=post.PostResponse,
                   status_code=status.HTTP_200_OK)
async def update_post(updated_post: post.UpdatePostRequest, post_id: int,
                      post_service: PostService = Depends(PostService)):
    user_id = updated_post.dict(include={'user_id'})['user_id']
    try:
        result = await post_service.update(post_id, user_id,
                                           update_data=updated_post.dict(exclude={'user_id'}, exclude_none=True))
    except ValidationError as e:
        logger.warning(e.errors())
        raise HTTPException(status_code=422, detail=e.errors())
    except NotFoundPost:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Пост не найден')
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail='Неизвестная ошибка')
    else:
        return result


@post_router.post("/",
                  description='Добавление нового поста',
                  response_model=post.PostCreateResponse,
                  status_code=status.HTTP_201_CREATED)
async def add_post(new_post: post.CreatePostRequest, post_service: PostService = Depends(PostService)):
    try:
        result = await post_service.create(new_post.dict())
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail='Неизвестная ошибка')
    else:
        return result


@post_router.delete("/{post_id}",
                    description='Удаление поста по id',
                    status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, user_id: int, post_service: PostService = Depends(PostService)):
    try:
        await post_service.delete(post_id, user_id=user_id)
    except NotFoundPost:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Пост не найден')
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail='Неизвестная ошибка')
    else:
        return


@post_router.get("/{post_id}/like",
                 description='Лайк поста по id',
                 response_model=post.PostResponse,
                 status_code=status.HTTP_200_OK)
async def like(post_id: int, user_id: int, post_service: PostService = Depends(PostService)):
    try:
        result = await post_service.like_post(post_id, user_id)
    except NotFoundPost:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Пост не найден')
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail='Неизвестная ошибка')
    else:
        return result


@post_router.get("/{post_id}/dislike",
                 description='Дизлайк поста по id',
                 response_model=post.PostResponse,
                 status_code=status.HTTP_200_OK)
async def dislike(post_id: int, user_id: int, post_service: PostService = Depends(PostService)):
    try:
        result = await post_service.dislike_post(post_id, user_id)
    except NotFoundPost:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Пост не найден')
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail='Неизвестная ошибка')
    else:
        return result
