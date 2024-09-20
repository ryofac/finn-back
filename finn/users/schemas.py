from datetime import datetime

from fastapi import Form
from pydantic import BaseModel

from finn.core.schemas import OrmModel
from finn.debit.schemas import DebitSchema


class UserBase(OrmModel):
    id: int
    username: str
    full_name: str
    password: str
    debits: list[DebitSchema]
    created_at: datetime
    updated_at: datetime


class UserPublic(OrmModel):
    """Modelo usado no retorno de dados do usuário"""

    id: int
    username: str
    full_name: str
    email: str
    debits: list[DebitSchema]
    profile_photo_url: str | None
    created_at: datetime
    updated_at: datetime


class UserList(OrmModel):
    users: list[UserPublic]


class UserCreate(OrmModel):
    """Modelo usado na criação de dados do usuário"""

    username: str
    email: str
    full_name: str
    password: str

    @classmethod
    def as_form(
        cls,
        username: str = Form(...),
        email: str = Form(...),
        full_name: str = Form(...),
        password: str = Form(...),
    ) -> "UserCreate":
        return cls(
            username=username,
            email=email,
            full_name=full_name,
            password=password,
        )


class UserUpdate(OrmModel):
    """Modelo usado na atualização de dados do usuário"""

    full_name: str
    password: str


class UserFilterSchema(BaseModel):
    dt_created_from: datetime | None
    dt_created_to: datetime | None
    name: str | None
    name_i: str | None
    username: str | None
    username_i: str | None
