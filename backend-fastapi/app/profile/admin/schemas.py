from pydantic import BaseModel
from typing import Optional

class UserRoleUpdate(BaseModel):
    role_name: str

class AdminUserRead(BaseModel):
    id: int
    name: str
    email: str
    role_name: Optional[str] = None

    class Config:
        orm_mode = True
