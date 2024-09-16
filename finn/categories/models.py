from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from finn.database import BaseModelMixin, table_registry

if TYPE_CHECKING:
    from finn.debit.models import Debit


@table_registry.mapped_as_dataclass
class Category(BaseModelMixin):
    __tablename__ = "categories"

    name: Mapped[str]
    description: Mapped[str]

    debits: Mapped[list["Debit"]] = relationship(
        "Debit",
        init=False,
        back_populates="category",
        lazy="selectin",
    )
