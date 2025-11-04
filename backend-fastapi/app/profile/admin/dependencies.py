from fastapi import Depends, HTTPException, status
from app.auth.oauth2 import get_current_user
from app.profile.users.models import User

def get_current_admin_user(current_user: User = Depends(get_current_user)):
    """
    Dependency that ensures the current user is an admin.
    """
    if not current_user.role or current_user.role.name.lower() != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required."
        )
    return current_user
