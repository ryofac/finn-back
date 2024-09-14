from decimal import Decimal

from finn.schemas.base_schema import OrmModel
from finn.schemas.category_schema import CategorySchema


class DebitSchema(OrmModel):
    id: int
    value: Decimal
    category: CategorySchema


class DebitList(OrmModel):
    debits: list[DebitSchema]
