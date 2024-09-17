from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from finn.database import get_session
from finn.users.filters import UserFilterSchema, filter_user
from finn.users.models import User
from finn.users.schemas import UserCreate, UserList, UserPublic, UserUpdate

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserPublic,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "User with the same user exists."},
    },
)
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    db_user: User = User(**user.model_dump(exclude="password"))

    existent_user = await session.scalar(select(User).where((User.username == user.username) | (User.email == user.email)))

    if existent_user:
        if existent_user.username == user.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with the same username exists",
            )
        elif existent_user.email == user.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with the same email exists",
            )

    db_user.password = user.password
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


@user_router.get(
    "/",
    response_model=UserList,
)
async def get_users(
    dt_created_from: datetime | None = Query(None, description="Data de criação a partir de"),
    dt_created_to: datetime | None = Query(None, description="Data de criação limite"),
    name: str | None = Query(None, description="Busca por nome exato"),
    name_i: str | None = Query(None, description="Busca por nome parecido"),
    username: str | None = Query(None, description="Busca por username exato"),
    username_i: str | None = Query(None, description="Busca por username parecido"),
    limit: int = 100,
    offset: int = 0,
    session: AsyncSession = Depends(get_session),
):
    query = filter_user(
        UserFilterSchema(
            dt_created_from=dt_created_from,
            dt_created_to=dt_created_to,
            name_i=name_i,
            name=name,
            username=username,
            username_i=username_i,
        )
    )
    result = await session.scalars(query.limit(limit).offset(offset))

    all_users = UserList.model_validate({"users": result})

    return all_users


@user_router.get(
    "/{user_id}",
    response_model=UserPublic,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "User not found"},
    },
)
async def get_user_by_id(user_id: int, session: AsyncSession = Depends(get_session)):
    user_db = await session.scalar(select(User).where(User.id == user_id))

    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found!",
        )

    return user_db


@user_router.put(
    "/{user_id}",
    response_model=UserPublic,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "User not found"},
    },
)
async def update_user(user_id: int, user_update: UserUpdate, session: AsyncSession = Depends(get_session)):
    exist_user: User = await session.scalar(select(User).where(user_id == User.id))

    if not exist_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found!",
        )

    exist_user.password = user_update.password
    exist_user.full_name = user_update.full_name

    await session.commit()
    await session.refresh(exist_user)

    return exist_user


@user_router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "User not found"},
    },
)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    exist_user = await session.scalar(select(User).where(user_id == User.id))

    if not exist_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found!",
        )

    await session.delete(exist_user)
    await session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
