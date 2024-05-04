from fastapi import FastAPI
from models import auth_models
from routes.auth_routes import auth_router
from routes.orders_routes import order_router
from .database import engine

app = FastAPI()

auth_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "Welcome Home"}

app.include_router(auth_router)
app.include_router(order_router)