from typing import List, Optional
from sqlmodel import Session, select
from .models import User
from .schemas import (
    UserCreate,
    UserUpdate
    )

# use this if we're using lightweight role implementation
# def create_user(db: Session, user: UserCreate) -> User:
#     db_user = User(**user.model_dump())
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# use this if we're linking to Role model
from app.auth.password_utils import get_password_hash
from app.profile.roles.models import Role
from fastapi import HTTPException, status

def create_user(db: Session, user_data: UserCreate):
    role = None
    if user_data.role_id:
        role = db.get(Role, user_data.role_id)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Role with id={user_data.role_id} does not exist.",
            )
    elif user_data.role_name:
        role = db.exec(select(Role).where(Role.name == user_data.role_name)).first()
        if not role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Role '{user_data.role_name}' does not exist.",
            )

    hashed_password = get_password_hash(user_data.password)
    user = User(
        name=user_data.name,
        email=user_data.email,
        password=hashed_password,
        role_id=role.id if role else None,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user



def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.get(User, user_id)

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    statement = select(User).where(User.email == email)
    return db.exec(statement).first()

def get_all_users(db: Session) -> List[User]:
    statement = select(User)
    return db.exec(statement).all()

def delete_user(db: Session, user_id: int) -> bool:
    user = db.get(User, user_id)
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True

def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    user = db.get(User, user_id)
    if not user:
        return None
    user_data = user_update.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(user, key, value)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

