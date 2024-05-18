from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
# from jose import jwt
from sqlalchemy.orm import Session
from schemas.auth_schemas import SignUpModel
from models.auth_models import User
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os


load_dotenv()


# Security
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM=os.getenv("ALGORITHM")
SECRET_KEY=os.getenv("SECRET_KEY")


# Function to verify password
def verify_password(plain_password, hashed_password):
    return check_password_hash(plain_password, hashed_password)

# Function to create a new user
def create_user(db: Session, user: SignUpModel):
    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# Function to authenticate user
def authenticate_user(db: Session, username: str, password: str):
    db_user = db.query(User).filter(User.username == username).first()

    if not db_user or not verify_password(password, db_user.password):
        return False
    
    return db_user


# Function to create access token
def create_access_token():
    pass