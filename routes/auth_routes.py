from fastapi import APIRouter
from ..database import engine, db_session
from ..schemas.auth_schemas import SignUpModel
from ..models.auth_models import User

auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@auth_router.get("/")
async def hello():
    return {"message": "Hello World"}


@auth_router.post("/signup")
async def signup(user: SignUpModel, db: db_session):
    db_email = db.query(User).filter(email=user.email).first()


@auth_router.post("/login")
async def login():
    pass