#here we are defining the database string
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DB_URL")
engine = create_engine(DATABASE_URL)#imp
Base = declarative_base()#imp to map the class with table
SessionLocal = sessionmaker(bind=engine)    