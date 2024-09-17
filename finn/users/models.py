from typing import TYPE_CHECKING

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from finn import security
from finn.core.models import Base, DatedModelMixin

if TYPE_CHECKING:
    from finn.debit.models import Debit


class User(Base, DatedModelMixin):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    full_name: Mapped[str] = mapped_column(nullable=False)
    _password: Mapped[str] = mapped_column(init=False, name="password")
    debits: Mapped[list["Debit"]] = relationship(
        "Debit",
        init=False,
        back_populates="owner",
        lazy="selectin",
    )

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, new_password: str):
        self._password = security.get_password_hash(new_password)

    def verify_password(self, plain_password: str):
        return security.verify_password(plain_password)
