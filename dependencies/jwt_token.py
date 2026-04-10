from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from utils.token import SECRET_KEY, ALGORITHM
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# this dependecy validates the token passed in authorization in header from client 
# authorizes it and gives the response
security = HTTPBearer()
def get_current_user(creds : HTTPAuthorizationCredentials = Depends(security)):
    print(creds)
    token = creds.credentials
    print(token)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        role = payload.get("role")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid user token")
        return {"username":username, "role": role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# what is dependency injection??
# instead of creating object inside a function (Tight coupling) 
# we them from outside(Loose Coupling)