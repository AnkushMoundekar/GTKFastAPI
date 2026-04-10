from jose import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv

import os

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=30)

    to_encode.update({"exp": expire})
    print(to_encode)
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

