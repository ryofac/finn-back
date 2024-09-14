from datetime import datetime
from typing import List

from finn.schemas.base_schema import OrmModel
from finn.schemas.debit_schema import DebitSchema


class UserBase(OrmModel):
    id: int
    username: str
    full_name: str
    password: str
    debits: List[DebitSchema]
    created_at: datetime
    updated_at: datetime


class UserPublic(OrmModel):
    """Modelo usado no retorno de dados do usuário"""

    id: int
    username: str
    full_name: str
    email: str
    debits: List[DebitSchema]
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


class UserUpdate(OrmModel):
    """Modelo usado na atualização de dados do usuário"""

    full_name: str
    password: str
