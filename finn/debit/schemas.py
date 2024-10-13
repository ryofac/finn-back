from datetime import datetime

from pydantic import BaseModel

from finn.categories.schemas import CategorySchema
from finn.core.schemas import OrmModel


class DebitSchema(OrmModel):
    id: int
    value: float
    category: CategorySchema | None
    dt_payment: datetime


class DebitCreateOrUpdateSchema(OrmModel):
    value: float
    category_id: int


class DebitList(OrmModel):
    debits: list[DebitSchema]


class DebitFilterSchema(BaseModel):
    dt_payment_from: datetime | None
    dt_payment_to: datetime | None
    owner_id: int | None
    category_id: int | None
    category_name: str | None
