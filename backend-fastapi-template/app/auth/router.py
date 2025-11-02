from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# from users module
from app.users.schemas import UserCreate, UserRead
from app.users.crud import create_user, get_user_by_email

from .schemas import UserLogin
from .jwt_handler import create_access_token
from .password_utils import get_password_hash, verify_password
from .oauth2 import get_current_user
from app.core.database import get_session

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserRead)
def register(user: UserCreate, db: Session = Depends(get_session)):
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user.password = get_password_hash(user.password)
    return create_user(db, user)

@router.post("/login")
def login(form_data: UserLogin, db: Session = Depends(get_session)):
    user = get_user_by_email(db, form_data.email)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token({"user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me")
def auth_me(current_user = Depends(get_current_user)):
    return {"user": current_user, "status": "authenticated"}



