# this script defines a mapping between Python class and database table 
# here we are doing this using Sqlalchemy
# it allows you to interact with database tables using python class without using raw sql
from sqlalchemy import Column,String,Integer
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index= True)
    name = Column(String)
    age = Column(Integer)

class AuthUser(Base):
    __tablename__="Auth_users"

    id = Column(Integer, primary_key= True, index= True)
    name = Column(String, unique= True)
    password = Column(String)
    role = Column(String, default= "user")


