from time import time
from fastapi import HTTPException

request_store = {}

def rate_limiter(key: str, limit: int, window: int):
    current_time = time()
    
    if key not in request_store:
        request_store[key]=[]
    #remove the old requests
    request_store[key]=[t for t in request_store[key] if current_time - t < window]


    if len(request_store[key])>limit:
        raise HTTPException(status_code=429, detail="Too many requests")
    #store the current time when each request is triggered
    request_store[key].append(current_time)
    print(request_store)
