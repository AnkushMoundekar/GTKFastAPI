from passlib.context import CryptContext

pwd = CryptContext(schemes=["argon2"], deprecated = "auto")
# print(pwd.hash("test123"))

def hash_password(password: str):
    return pwd.hash(password)

def verify_password(plain, hash):
    return pwd.verify(plain, hash)