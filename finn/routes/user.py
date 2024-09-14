from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from finn.database import get_session
from finn.models import User
from finn.schemas.user_schema import UserCreate, UserList, UserPublic

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserPublic,
)
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    db_user: User = User(**user.model_dump())

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

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


@router.get(
    "/",
    response_model=UserList,
)
async def get_users(limit: int = 100, offset: int = 0, session: AsyncSession = Depends(get_session)):
    result = await session.scalars(select(User).offset(offset).limit(limit))
    all_users = result.all()
    all_users = UserList.model_validate({"users": all_users})

    return all_users


@router.get("/{user_id}", response_model=UserPublic)
async def get_user_by_id(user_id: int, session: AsyncSession = Depends(get_session)):
    user_db = await session.scalar(select(User).where(User.id == user_id))

    if not user_db:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found!",
        )

    return user_db


@router.put("/{user_id}", response_model=UserPublic)
async def update_user(user_id: int, session: AsyncSession = Depends(get_session)):
    pass
