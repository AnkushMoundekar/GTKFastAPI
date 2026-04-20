from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.user_model import User, AuthUser
from models.tokens_model import RefreshToken
from database import engine, Base
from dependencies.db import get_db
from schemas.user_schema import UserResponse, UserSchema, AuthSchema, RefreshRequest
from utils.security import hash_password, verify_password
from utils.token import create_access_token, create_refresh_token
from dependencies.check_admin import require_role
from dependencies.jwt_token import create_new_access_token
from dependencies.permissions import require_permission

router = APIRouter()

Base.metadata.create_all(bind = engine)# it will create tables in db if not exist

@router.post("/api/create_user", response_model=UserResponse)
def create_user(user : UserSchema, db : Session = Depends(get_db)):
    db_user =  User(name = user.name, age = user.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@router.get("/api/get_users", response_model=list[UserResponse])
def get_users(db : Session = Depends(get_db)):
    return db.query(User).all()

@router.delete("/api/delete_user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), permitted_user = Depends(require_permission("delete_users"))):
        user = db.query(AuthUser).filter(AuthUser.id == user_id).first()

        if not user:
            return {"message": "user not found"}
        db.delete(user)
        db.commit()

        return {"message": "user deleted"}

@router.post("/signup")
def signup(auth : AuthSchema, db: Session = Depends(get_db)):
    hash = hash_password(auth.password)
    db_auth = AuthUser(name = auth.name, password = hash, role = auth.role if auth.role else "user", permissions = "abc")
    db.add(db_auth)
    db.commit()
    db.refresh(db_auth)
    
    return {"message": "auth user saved"}

@router.post("/login")
def login(auth: AuthSchema, db: Session = Depends(get_db)):
    db_user = db.query(AuthUser).filter(AuthUser.name == auth.name).first()

    if not db_user:
        return {"message":"user not found"}
    
    if not verify_password(auth.password, db_user.password):
        return {"message": "incorrect password"}
    
    access_token = create_access_token({"sub": db_user.name, "role": db_user.role})
    refresh_token = create_refresh_token({"sub": db_user.name})
    # while login in we will save the refresh token to db to check in future if the token is valid for refresh requests
    db_token = RefreshToken(
        user_id = db_user.id,
        token = refresh_token
    )
    db.add(db_token)
    db.commit()
    return {
        "access token": access_token,
        "refresh token": refresh_token
    }
@router.post("/logout")
def logout(request: RefreshRequest, db : Session = Depends(get_db)):
    db_token = db.query(RefreshToken).filter(RefreshToken.token == request.token).first()
    if not db_token:
        raise HTTPException(status_code=401, detail= "invalid user id")
    #at the time of logout we will delete the refresh tokens which will automatically disable the access to the protected route
    db.delete(db_token)
    db.commit()
    return {"message": "user logout successfully"}

@router.post("/refresh")
def refresh_token(refresh_token, db: Session = Depends(get_db)):
    db_token = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
    if not db_token:
        raise HTTPException(status_code= 404, detail="Invalid refresh token")
    return {"access token": create_new_access_token(refresh_token = refresh_token, db= db)}

    

