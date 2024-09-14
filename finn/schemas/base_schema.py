from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import List

from pydantic import BaseModel, ConfigDict

from finn.models import Debit


class Message(BaseModel):
    message: str


class DebitSchema(BaseModel):
    id: int
    value: Decimal


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    full_name: str
    password: str
    debits: List[DebitSchema]
    created_at: datetime
    updated_at: datetime


class UserPublic(BaseModel):
    """Modelo usado no retorno de dados do usuário"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    full_name: str
    email: str
    debits: List[DebitSchema]
    created_at: datetime
    updated_at: datetime


class UserList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    users: list[UserPublic]


class UserCreate(BaseModel):
    """Modelo usado na criação de dados do usuário"""

    model_config = ConfigDict(from_attributes=True)

    username: str
    email: str
    full_name: str
    password: str


class UserUpdate(BaseModel):
    """Modelo usado na atualização de dados do usuário"""

    model_config = ConfigDict(from_attributes=True)

    full_name: str
    password: str
