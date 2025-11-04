from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.profile.users.models import User


class RoleBase(SQLModel):
    name: str = Field(index=True, unique=True)
    description: Optional[str] = None


class Role(RoleBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # relationship
    users: List["User"] = Relationship(back_populates="role")





class Permission(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None