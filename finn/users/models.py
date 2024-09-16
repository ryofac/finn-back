from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from finn.core.models import DatedModelMixin
from finn.database import BaseModelMixin, table_registry

if TYPE_CHECKING:
    from finn.debit.models import Debit


@table_registry.mapped_as_dataclass
class User(BaseModelMixin, DatedModelMixin):
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
