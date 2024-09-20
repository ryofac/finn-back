import os
from typing import TYPE_CHECKING

from sqlalchemy import String, event
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from finn import security
from finn.core.models import Base, DatedModelMixin

if TYPE_CHECKING:
    from finn.debit.models import Debit


class User(Base, DatedModelMixin):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(), unique=True)
    profile_photo_url: Mapped[str] = mapped_column(String(500), init=False, nullable=True)
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
        return security.verify_password(plain_password, self._password)


@event.listens_for(User, "before_delete")
def handle_before_user_delete(mapper, connection, target: User):
    if target.profile_photo_url:
        try:
            os.remove(target.profile_photo_url)
        except Exception as e:
            print("Deu erro ao remover o arquivo: " + str(e))
