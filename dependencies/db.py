#this dependency creates db sessions give it to your api and finally close it after request
from database import SessionLocal
# using this dependecy because global sessions are not good 
# if the same session used by 2 different api can cause conflicts and errors
# if we use the dependency injection we create new session for different api request

def get_db():
    db=SessionLocal()
    try:
        yield db # it pauses till we get the response from API 
    finally:
        db.close()


# yeild pauses the function at the line until next is called
# in fastapi it is called internally