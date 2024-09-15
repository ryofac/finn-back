from datetime import datetime
from decimal import Decimal

from finn.categories.schemas import CategorySchema
from finn.core.schemas import OrmModel


class DebitSchema(OrmModel):
    id: int
    value: float
    owner_id: int
    category: CategorySchema
    dt_payment: datetime


class DebitCreateOrUpdateSchema(OrmModel):
    value: Decimal
    category_id: int
    owner_id: int


class DebitList(OrmModel):
    debits: list[DebitSchema]
