from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from finn.database import get_session
from finn.debit.models import Debit
from finn.debit.schemas import DebitCreateOrUpdateSchema, DebitList, DebitSchema
from finn.models import Category, User

debit_router = APIRouter(prefix="/debits", tags=["debits"])


@debit_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=DebitCreateOrUpdateSchema,
)
async def create_debit(debit: DebitCreateOrUpdateSchema, session: AsyncSession = Depends(get_session)):
    db_debit: Debit = Debit(**debit.model_dump())

    owner: User = await session.scalar(select(User).where(User.id == db_debit.owner_id))
    category: Category = await session.scalar(select(Category).where(Category.id == db_debit.category_id))

    if not owner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found!",
        )

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found!",
        )

    session.add(db_debit)
    await session.commit()
    await session.refresh(db_debit)
    return db_debit


@debit_router.get(
    "/",
    response_model=DebitList,
)
async def get_debits(limit: int = 100, offset: int = 0, session: AsyncSession = Depends(get_session)):
    result = await session.scalars(select(Debit).offset(offset).limit(limit))
    debits = result.all()
    return {"debits": debits}


@debit_router.get(
    "/{debit_id}",
    response_model=DebitSchema,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Debit not found!"},
    },
)
async def get_debit_by_id(debit_id: int, session: AsyncSession = Depends(get_session)):
    debit_db = await session.scalar(select(Debit).where(Debit.id == debit_id))

    if not debit_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Debit not found!",
        )

    return debit_db


@debit_router.put(
    "/{debit_id}",
    response_model=DebitSchema,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Debit not found!"},
    },
)
async def update_debit(debit_id: int, debit_update: DebitCreateOrUpdateSchema, session: AsyncSession = Depends(get_session)):
    exist_debit: Debit = await session.scalar(select(Debit).where(debit_id == Debit.id))

    if not exist_debit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Debit not found!",
        )

    exist_debit.value = debit_update.value
    exist_debit.category_id = debit_update.category_id

    await session.commit()
    await session.refresh(exist_debit)

    return exist_debit


@debit_router.delete(
    "/{debit_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Debit not found!"},
    },
)
async def delete_debit(debit_id: int, session: AsyncSession = Depends(get_session)):
    exist_debit = await session.scalar(select(Debit).where(debit_id == Debit.id))

    if not exist_debit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Debit not found!",
        )

    await session.delete(exist_debit)
    await session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
