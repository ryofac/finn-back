from sqlalchemy import select

from finn.categories.models import Category
from finn.debit.models import Debit
from finn.debit.schemas import DebitFilterSchema


def filter_debit(parameters: DebitFilterSchema):
    query = select(Debit)
    if parameters.dt_payment_from:
        query = query.filter(Debit.dt_payment > parameters.dt_payment_from)

    if parameters.dt_payment_to:
        query = query.filter(Debit.dt_payment <= parameters.dt_payment_to)

    if parameters.category_id:
        query = query.filter(Debit.category_id == parameters.category_id)

    if parameters.category_name:
        query = query.join(Category, Category.id == Debit.category_id).filter(Category.name.icontains(parameters.category_name))

    return query
