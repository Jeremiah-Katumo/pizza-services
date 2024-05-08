from fastapi import FastAPI
from models import auth_models
from routes import auth_routes
from routes import orders_routes
from database import engine
from fastapi_jwt_auth import AuthJWT
from .schemas.settings_schemas import Settings

app = FastAPI()

auth_models.Base.metadata.create_all(bind=engine)

@app.get("/", tags=['Home'])
def home():
    return {"message": "Welcome Home"}

@AuthJWT.load_config
def get_config():
    return Settings()

app.include_router(auth_routes.auth_router)
app.include_router(orders_routes.order_router)