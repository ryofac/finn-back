from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from finn.categories.models import Category
from finn.database import get_session
from finn.debit.filters import filter_debit
from finn.debit.models import Debit
from finn.debit.schemas import DebitCreateOrUpdateSchema, DebitFilterSchema, DebitList, DebitSchema
from finn.users.models import User

debit_router = APIRouter(prefix="/debits", tags=["debits"])


@debit_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=DebitCreateOrUpdateSchema,
)
async def create_debit(debit: DebitCreateOrUpdateSchema, session: AsyncSession = Depends(get_session)):
    db_debit: Debit = Debit(**debit.model_dump())

    if not debit.owner_id or not debit.category_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debit must have user and category",
        )

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
async def get_debits(
    dt_payment_from: datetime | None = Query(None, description="Data de pagamento de"),
    dt_payment_to: datetime | None = Query(None, description="Data de pagamento limite"),
    owner_id: int | None = Query(None, description="Id do Usuário da task"),
    category_id: int | None = Query(None, description="Id da categoria"),
    category_name: str | None = Query(None, description="Nome da categoria"),
    limit: int = 100,
    offset: int = 0,
    session: AsyncSession = Depends(get_session),
):
    query = filter_debit(
        DebitFilterSchema(
            dt_payment_from=dt_payment_from,
            dt_payment_to=dt_payment_to,
            owner_id=owner_id,
            category_id=category_id,
            category_name=category_name,
        )
    )
    result = await session.scalars(query.offset(offset).limit(limit))
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

    category = await session.scalar(select(Category).where(Category.id == debit_update.category_id))
    if not category:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "This category does not exists!")
    exist_debit.category_id = category.id

    owner = await session.scalar(select(User).where(User.id == debit_update.owner_id))
    if not owner:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "This user does not exists!")
    exist_debit.owner_id = owner.id

    exist_debit.value = debit_update.value

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
