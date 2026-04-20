from fastapi import Depends, HTTPException
from dependencies.jwt_token import get_current_user

def require_permission(req_permission: str):
    def permission_checker(user = Depends(get_current_user)):
        permissions = user.permissions.split(",")
        if req_permission not in permissions:
            raise HTTPException(status_code= 403, detail="not authorised")
        return user
    return permission_checker