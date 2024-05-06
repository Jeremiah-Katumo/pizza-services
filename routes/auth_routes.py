from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from database import engine, db_session
from schemas.auth_schemas import SignUpModel, LogInModel
from models.auth_models import User
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder


auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@auth_router.get("/")
async def hello():
    return {"message": "Hello World"}


@auth_router.post("/signup", response_model=SignUpModel, status_code=status.HTTP_201_CREATED)
async def signup(user: SignUpModel, db: db_session):
    db_email = db.query(User).filter(User.email==user.email).first()

    if db_email is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
            detail="User with the email already exists")
    
    db_username = db.query(User).filter(User.username==user.username).first()

    if db_username is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with the username already exists")

    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff
    )

    db.add(new_user)
    db.commit()

    return new_user


@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login(user: LogInModel, Authorize: AuthJWT=Depends()):
    db_user = db_session.query(User).filter(User.username==user.username).first()

    if db_user and check_password_hash(db_user.password, user.password):
        access_token = Authorize.create_access_token(subject=db_user.username)
        refresh_token = Authorize.create_refresh_token(subject=db_user.username)

        response={
            "access": access_token,
            "refresh": refresh_token
        }

        return jsonable_encoder(response)
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid Username Or Password")