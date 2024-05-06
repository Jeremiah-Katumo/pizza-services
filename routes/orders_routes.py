from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT
from models.auth_models import User, Order
from schemas.orders_schemas import OrderModel
from database import db_session


order_router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

@order_router.get("/")
async def hello(Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"    
        )
    
    return {"message": "Hello World"}


@order_router.post('/order')
async def place_an_order(order: OrderModel, db: db_session, Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"    
        )
    
    current_user = Authorize.get_jwt_subject()

    user = db.query(User).filter(User.username==current_user).first()

    new_order = Order(
        pizza_size=order.pizza_size,
        quantity=order.quantity
    )

    new_order.user = user

    db.add(user)
    db.commit()