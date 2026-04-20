from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from utils.token import SECRET_KEY, ALGORITHM
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dependencies.db import get_db
from models.user_model import AuthUser
from utils.token import create_access_token
# this dependecy validates the token passed in authorization in header from client 
# authorizes it and gives the response
security = HTTPBearer()
def get_current_user(creds : HTTPAuthorizationCredentials = Depends(security), db = Depends(get_db)):
    token = creds.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        print(payload)
        role = payload.get("role")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid user token")
        user = db.query(AuthUser).filter(AuthUser.name == username).first()
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def create_new_access_token(refresh_token, db):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms= [ALGORITHM])

        user = payload.get("sub")
        if user is None:
            raise HTTPException(status_code=401, details="Invalid token")
        role = db.query(AuthUser).filter(AuthUser.name ==  user).first().role
        print(role)
        new_access_token = create_access_token({"sub": user , "role": role})
        return new_access_token
    except Exception as e:
        print(e)
        raise HTTPException(status_code= 401, detail= f"Invalid token & {e}")

# what is dependency injection??
# instead of creating object inside a function (Tight coupling) 
# we them from outside(Loose Coupling)