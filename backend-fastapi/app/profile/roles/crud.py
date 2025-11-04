from sqlmodel import Session, select
from .models import Role
from .schemas import RoleCreate

def get_role_by_id(db: Session, role_id: int):
    return db.get(Role, role_id)

def get_role_by_name(db: Session, name: str):
    statement = select(Role).where(Role.name == name)
    return db.exec(statement).first()

def create_role(db: Session, role: RoleCreate):
    db_role = Role(**role.model_dump())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def get_all_roles(db: Session):
    statement = select(Role)
    return db.exec(statement).all()

def delete_role(db: Session, role_id: int):
    role = db.get(Role, role_id)
    if role:
        db.delete(role)
        db.commit()
        return True
    return False
