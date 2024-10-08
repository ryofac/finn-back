from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from finn.core.models import Base

if TYPE_CHECKING:
    from finn.debit.models import Debit


class Category(Base):
    __tablename__ = "categories"

    name: Mapped[str]
    description: Mapped[str]

    debits: Mapped[list["Debit"]] = relationship(
        "Debit",
        init=False,
        back_populates="category",
        lazy="selectin",
    )
