from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.core.database import get_session
from .schemas import RoleCreate, RoleRead
from . import crud, schemas

router = APIRouter(prefix="/roles", tags=["roles"])



@router.get("/{role_id}", response_model=RoleRead)
def read_role(role_id: int, db: Session = Depends(get_session)):
    role = crud.get_role_by_id(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@router.get("/", response_model=list[RoleRead])
def read_roles(db: Session = Depends(get_session)):
    return crud.get_all_roles(db)

@router.post("/", response_model=RoleRead)
def create_role(role: RoleCreate, db: Session = Depends(get_session)):
    existing = crud.get_role_by_name(db, role.name)
    if existing:
        raise HTTPException(status_code=400, detail="Role already exists")
    return crud.create_role(db, role)

@router.delete("/{role_id}")
def delete_role(role_id: int, db: Session = Depends(get_session)):
    success = crud.delete_role(db, role_id)
    if not success:
        raise HTTPException(status_code=404, detail="Role not found")
    return {"ok": True}
