from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column, relationship


class Base(MappedAsDataclass, DeclarativeBase):
    id: Mapped[int] = mapped_column(init=False, primary_key=True)


class DatedModelMixin:
    created_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now(),
        onupdate=func.now(),
    )


class User(Base, DatedModelMixin):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    full_name: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str]
    debits: Mapped[list["Debit"]] = relationship(
        "Debit",
        back_populates="owner",
        lazy="selectin",
    )


class Category(Base):
    __tablename__ = "categories"

    name: Mapped[str]
    description: Mapped[str]

    debits: Mapped["Debit"] = relationship("Debit")


class Debit(Base):
    __tablename__ = "debits"

    value: Mapped[Decimal]
    dt_payment: Mapped[datetime]

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    owner: Mapped[User] = relationship(
        "User",
        back_populates="debits",
        lazy="selectin",
    )

    category: Mapped[Category] = relationship(
        "Category",
        back_populates="debits",
        lazy="selectin",
    )
