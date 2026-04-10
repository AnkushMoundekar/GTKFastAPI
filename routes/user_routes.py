from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.user_model import User, AuthUser
from database import engine, Base
from dependencies.db import get_db
from schemas.user_schema import UserResponse, UserSchema, AuthSchema
from utils.security import hash_password, verify_password
from utils.token import create_access_token

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
def delete_user(use_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == use_id).first()

    if not user:
        return {"message": "user not found"}
    db.delete(user)
    db.commit()

    return {"message": "user deleted"}

@router.post("/signup")
def signup(auth : AuthSchema, db: Session = Depends(get_db)):
    hash = hash_password(auth.password)
    db_auth = AuthUser(name = auth.name, password = hash, role = auth.role if auth.role else "user")
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
    
    token = create_access_token({"sub": db_user.name, "role": db_user.role})
    return {
        "access token": token,
        "token_type": "bearer"
    }
