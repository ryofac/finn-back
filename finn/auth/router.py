from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from finn.auth.schemas import UserAuthSchema
from finn.core.schemas import Message
from finn.database import get_session
from finn.users.models import User
from finn.users.router import create_user
from finn.users.schemas import UserCreate, UserPublic

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post(
    "/register",
    status_code=status.HTTP_200_OK,
    response_model=UserPublic,
)
async def register(user: UserCreate, session: AsyncSession = Depends(get_session)):
    return await create_user(user, session)


@auth_router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=Message,
)
async def login(user: UserAuthSchema, session: AsyncSession = Depends(get_session)):
    existent_user = await session.scalar(select(User).where(User.username == user.username))
    if not existent_user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "👎")

    if existent_user.verify_password(user.password):
        return {"message": "👍"}
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "👎")
