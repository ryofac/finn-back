from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from finn.core.models import Base, DatedModelMixin

if TYPE_CHECKING:
    from finn.debit.models import Debit


class User(Base, DatedModelMixin):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    full_name: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str]
    debits: Mapped[List["Debit"]] = relationship(
        "Debit",
        init=False,
        back_populates="owner",
        lazy="selectin",
    )
