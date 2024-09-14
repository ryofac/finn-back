from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Message(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    message: str


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    full_name: str
    password: str
    created_at: datetime
    updated_at: datetime


class UserPublic(BaseModel):
    """Modelo usado no retorno de dados do usuário"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    full_name: str
    created_at: datetime
    updated_at: datetime


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

    username: str
    full_name: str
    password: str
