from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from finn.categories.models import Category
from finn.core.models import Base

if TYPE_CHECKING:
    from finn.users.models import User


class Debit(Base):
    __tablename__ = "debits"

    value: Mapped[Decimal]
    dt_payment: Mapped[datetime] = mapped_column(init=False, default=func.now())

    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.id"), nullable=True)
    owner_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)

    owner: Mapped["User"] = relationship(
        "User",
        init=False,
        back_populates="debits",
        lazy="selectin",
    )

    category: Mapped[Category] = relationship(
        "Category",
        init=False,
        back_populates="debits",
        lazy="selectin",
    )
