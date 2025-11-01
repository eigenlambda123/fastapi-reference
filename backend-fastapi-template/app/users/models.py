from sqlmodel import SQLModel, Field
from datetime import datetime
from enum import Enum

class RoleEnum(str, Enum):
    ADMIN = "admin"
    USER = "user"

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    email: str
    role: RoleEnum = Field(default=RoleEnum.USER)
