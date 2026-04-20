from fastapi import FastAPI, Depends, HTTPException
# from pydantic import BaseModel
# from typing import Optional
# import psycopg2

# app = FastAPI()

# @app.get("/", include_in_schema= False)
# def read_root():
#     return {"Hello": "World"}

# @app.get("/items/{item_id}", include_in_schema= False)
# def read_item(item_id: int):
#     return {"item_id": item_id, "message": "Success"}


# conn = psycopg2.connect(
#     dbname="Temp",
#     user="postgres",
#     password="Ankush@psql1"
# )
# cursor=conn.cursor()


# class User(BaseModel):
#     name: str
#     age : Optional[int] = None

# @app.post("/api/create_user")
# def create_user(user: User):
#     cursor.execute(
#         "insert into users (name, age) values (%s, %s)",
#         (user.name, user.age,)
#     )
#     conn.commit()
#     return {"message": 'user added!'}

# @app.post("/api/create_users")
# def create_users(users: list[User]):
#     for user in users:
#         cursor.execute(
#             "insert into users (name, age) values (%s, %s)",
#             (user.name, user.age,)
#         )
#     conn.commit()
#     return {"message": f"{len(users)} users created"}

# @app.get("/api/get_users/")
# def get_users():
#     cursor.execute(
#         "select * from users"
#     )
#     rows = cursor.fetchall()
#     users=[]
#     for row in rows:
#         users.append({
#             "id": row[0],
#             "name": row[1],
#             "age": row[2]
#         })
#     return users
# @app.delete("/api/delete_user/{user_id}")
# def delete_user(user_id):
#     cursor.execute(
#         "delete from users where id = %s",
#         (user_id,)
#     )
#     conn.commit()
#     if cursor.rowcount == 0:
#         return{"messge": "user not found"}
#     return{"messge": "user deleted","id":user_id}

###########################################################################################
            
# from sqlalchemy.orm import Session
# from models.user_model import User, Base, engine
# from dependencies.db import get_db
# from schemas.user_schema import UserResponse, UserSchema   
# Base.metadata.create_all(bind = engine)
# @app.post("/api/create_user", response_model=UserResponse)
# def create_user(user : UserSchema, db : Session = Depends(get_db)):
#     db_user =  User(name = user.name, age = user.age)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)

#     return db_user

# @app.get("/api/get_users", response_model=list[UserResponse])
# def get_users(db : Session = Depends(get_db)):
#     return db.query(User).all()

# @app.delete("/api/delete_user/{user_id}")
# def delete_user(use_id: int, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.id == use_id).first()

#     if not user:
#         return {"message": "user not found"}
#     db.delete(user)
#     db.commit()

#     return {"message": "user deleted"}

####################################################################################
#After folder stucture changed
from routes.user_routes import router as user_router
from dependencies.jwt_token import get_current_user
app= FastAPI()
app.include_router(user_router, prefix="/api")

@app.get("/protected")
def protected(user = Depends(get_current_user)):
    return {"message": f"Hello {user.role} {user.name}"}


