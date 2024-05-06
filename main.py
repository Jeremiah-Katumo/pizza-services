from fastapi import FastAPI
from models import auth_models
from routes.auth_routes import auth_router
from routes.orders_routes import order_router
from database import engine
from fastapi_jwt_auth import AuthJWT
from schemas import Settings

app = FastAPI()

auth_models.Base.metadata.create_all(bind=engine)

@app.get("/", tags=['Home'])
def home():
    return {"message": "Welcome Home"}

@AuthJWT.load_config
def get_config():
    return Settings()

app.include_router(auth_router)
app.include_router(order_router)