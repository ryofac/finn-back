from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from finn.database import get_session
from finn.models import User
from finn.schemas.base_schema import Message, UserCreate, UserList, UserPublic

app = FastAPI()


@app.get(
    "/hello",
    status_code=status.HTTP_200_OK,
    response_model=Message,
)
def hello():
    return {"message": "hello world!"}


@app.post(
    "/users/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserPublic,
    tags=["users"],
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


@app.get(
    "/users/",
    response_model=UserList,
    tags=["users"],
)
async def get_users(limit: int = 100, offset: int = 0, session: AsyncSession = Depends(get_session)):
    result = await session.scalars(select(User).offset(offset).limit(limit))
    all_users = result.all()
    all_users = UserList.model_validate({"users": all_users})

    return all_users


async def get_user():
    pass
