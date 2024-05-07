from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from database import engine, db_session
from schemas.auth_schemas import SignUpModel, LogInModel
from models.auth_models import User
from cruds import auth_cruds
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder


auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@auth_router.get("/")
async def hello(Authorize: AuthJWT=Depends()):
    # protect the route
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid Token")
    
    return {"message": "Hello World"}


# Route for token generation
@auth_router.post('/token')
async def login_for_access_token():
    pass


@auth_router.post("/signup", response_model=SignUpModel, status_code=status.HTTP_201_CREATED)
async def signup(user: SignUpModel, db: db_session):
    db_email = db.query(User).filter(User.email==user.email).first()    
    db_username = db.query(User).filter(User.username==user.username).first()

    if db_email | db_username is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="User with the email already exists")

    return auth_cruds.create_user(db, user)


@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login(user: LogInModel, db: db_session, Authorize: AuthJWT=Depends()):
    db_user = db.query(User).filter(User.username==user.username).first()

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


# refresh tokens

@auth_router.get('/refresh')
async def refresh_token(Authorize: AuthJWT=Depends()):
    # protect the route
    try:
        Authorize.jwt_refresh_token_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Please provide a valid refresh token")
    
    current_user = Authorize.get_jwt_subject()
    
    access_token = Authorize.create_access_token(subject=current_user)

    return jsonable_encoder({"access_token": access_token})