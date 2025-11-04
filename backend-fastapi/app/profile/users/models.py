from sqlmodel import SQLModel, Field
from datetime import datetime
from enum import Enum
from typing import Optional, TYPE_CHECKING
from sqlmodel import Relationship

if TYPE_CHECKING:
    from app.profile.roles.models import Role

# Lightweight role implementation
# class RoleEnum(str, Enum):
#     ADMIN = "admin"
#     USER = "user"

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    email: str
    password: str

    # Lightweight role implementation
    # role: RoleEnum = Field(default=RoleEnum.USER) 

    # Use this if we want to link to Role model
    role_id: Optional[int] = Field(default=None, foreign_key="role.id")
    role: Optional["Role"] = Relationship(back_populates="users")

