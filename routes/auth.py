from fastapi import APIRouter

auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@auth_router.get("/")
async def hello():
    return {"message": "Hello World"}