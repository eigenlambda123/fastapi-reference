from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: str
    password: str

class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None

# Use this if we're using the lightweight role implementation
# class UserCreate(UserBase):
#     pass

# Use this if we're linking to the Role model
class UserCreate(UserBase):
    role_id: int | None = None

# Use this if we're using the lightweight role implementation
# class UserRead(UserBase):
#     id: int
#     role: str

# Use this if we're linking to the Role model
from typing import Optional
from app.profile.roles.schemas import RoleRead

class UserRead(BaseModel):
    id: int
    name: str
    email: str
    role: Optional[RoleRead] = None  

    class Config:
        from_attributes = True


