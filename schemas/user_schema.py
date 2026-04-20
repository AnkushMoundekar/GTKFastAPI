from pydantic import BaseModel
from typing import Optional
#pydantic schema defines shape of incomming request 
class UserSchema(BaseModel):
    name: str
    age: int

class UserResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
        extra = "forbid"
class AuthSchema(BaseModel):
    name: str
    password: str
    role: Optional[str]=None

class RefreshRequest(BaseModel):
    token: str