from sqlmodel import Session, select
from app.profile.users.models import User
from app.profile.roles.models import Role

def get_all_users(db: Session):
    return db.exec(select(User)).all()

def delete_user(db: Session, user_id: int):
    user = db.get(User, user_id)
    if not user:
        return None
    db.delete(user)
    db.commit()
    return True

def update_user_role(db: Session, user_id: int, new_role_name: str):
    user = db.get(User, user_id)
    if not user:
        return None

    role = db.exec(select(Role).where(Role.name == new_role_name)).first()
    if not role:
        return "role_not_found"

    user.role_id = role.id
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
