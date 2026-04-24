from utils.rate_limiter import rate_limiter
from fastapi import Request,Depends
from dependencies.jwt_token import get_current_user

#this is for authenticated routes after login because it is trying to get the user
def rate_limit_dependency(limit: int=10, window: int= 60):
    def limiter(
        request: Request,
        user = Depends(get_current_user)
    ):
        key= f"{user.name}:{request.url.path}"

        rate_limiter(key, limit, window)
    return limiter

# this will be for login or signup because still not authenticated
def rate_limit_dependency_unauth(limit: int =10, window: int =60):
    def limiter(request: Request):
        key = f"{request.client.host}:{request.url.path}"
        rate_limiter(key, limit, window)

    return limiter
