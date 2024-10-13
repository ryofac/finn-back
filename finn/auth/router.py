from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter
from jwt import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from finn.auth.auth_bearer import JWTBearer
from finn.auth.auth_handler import decode_jwt, sign_jwt
from finn.auth.schemas import TokenResponse, UserAuthSchema
from finn.database import get_session
from finn.users.models import User
from finn.users.schemas import UserCreate, UserPublic

auth_router = APIRouter(prefix="/auth", tags=["auth"])


async def get_current_user(token: str = Depends(JWTBearer()), session: AsyncSession = Depends(get_session)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        decoded_token = decode_jwt(token)
        if not decoded_token:
            return credentials_exception
    except InvalidTokenError:
        return credentials_exception

    username = decoded_token.get("user_id", None)
    if not username:
        raise credentials_exception

    user = await session.scalar(select(User).where(User.username == username))
    if not user:
        raise credentials_exception
    return user


@auth_router.post(
    "/register",
    status_code=status.HTTP_200_OK,
    response_model=UserPublic,
)
async def register(user: UserCreate, session: AsyncSession = Depends(get_session)):
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


@auth_router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=TokenResponse,
)
async def login(user: UserAuthSchema, session: AsyncSession = Depends(get_session)):
    existent_user = await session.scalar(select(User).where(User.username == user.username))
    if not existent_user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "User credentials not valid 👎")

    if existent_user.verify_password(user.password):
        return sign_jwt(user.username)
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "User credentials not valid 👎")
