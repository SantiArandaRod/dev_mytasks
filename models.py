from typing import Optional

from pydantic import ConfigDict
from sqlmodel import SQLModel, Field
from datetime import datetime
from enum import Enum

class TaskStatus(str, Enum):
    p = "Pendiente"
    ip = "en ejecucion"
    f = "completada"
    c = "cancelada"

class UserStatus(str, Enum):
    a = "activo"
    i = "inactivo"
    d = "eliminado"

class UserBase(SQLModel):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True, min_length=1, max_length=100)
    email: str = Field(index=True, unique=True, max_length=100)
    status: UserStatus = Field(default=UserStatus.a)
    premium: bool = Field(default=False)

class TaskBase(SQLModel):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True, min_length=1, max_length=100)
    description: str = Field(max_length=100)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    status: TaskStatus = Field(default=TaskStatus.p)

class TaskSQL(SQLModel, table=True):
    __tablename__ = "tasks"
    id: Optional[int]= Field(default=None, primary_key=True)
    model_config = ConfigDict(from_attributes=True)
class UserSQL(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[int]= Field(default=None, primary_key=True)
    model_config = ConfigDict(from_attributes=True)