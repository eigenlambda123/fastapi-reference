from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.core.database import get_session
from app.profile.admin.dependencies import get_current_admin_user
from app.profile.admin import crud
from app.profile.admin.schemas import UserRoleUpdate, AdminUserRead
from typing import List

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users", response_model=List[AdminUserRead])
def list_all_users(db: Session = Depends(get_session), admin_user=Depends(get_current_admin_user)):
    users = crud.get_all_users(db)
    return [
        AdminUserRead(
            id=u.id,
            name=u.name,
            email=u.email,
            role_name=u.role.name if u.role else None
        )
        for u in users
    ]

@router.patch("/users/{user_id}/role", response_model=AdminUserRead)
def change_user_role(user_id: int, update: UserRoleUpdate, db: Session = Depends(get_session), admin_user=Depends(get_current_admin_user)):
    updated_user = crud.update_user_role(db, user_id, update.role_name)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if updated_user == "role_not_found":
        raise HTTPException(status_code=404, detail="Role not found")
    return AdminUserRead(
        id=updated_user.id,
        name=updated_user.name,
        email=updated_user.email,
        role_name=updated_user.role.name if updated_user.role else None
    )

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_session), admin_user=Depends(get_current_admin_user)):
    success = crud.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": f"User {user_id} deleted successfully"}
