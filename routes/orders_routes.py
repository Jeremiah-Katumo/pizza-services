from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT
from models.auth_models import User, Order
from schemas.orders_schemas import OrderModel
from database import db_session
from fastapi.encoders import jsonable_encoder


order_router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

@order_router.get("/")
async def hello(Authorize: AuthJWT=Depends()):
    # protect the route
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid Token")
    
    return {"message": "Hello World"}


@order_router.post('/order')
async def place_an_order(order: OrderModel, db: db_session, Authorize: AuthJWT=Depends()):
    # protect the route
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid Token")
    
    current_user = Authorize.get_jwt_subject()

    user = db.query(User).filter(User.username==current_user).first()

    new_order = Order(
        pizza_size=order.pizza_size,
        quantity=order.quantity
    )

    new_order.user = user

    db.add(user)
    db.commit()

    response = {
        "pizza_size": new_order.pizza_size,
        "quantity": new_order.quantity,
        "id": new_order.id,
        "order_status": new_order.order_status
    }

    return jsonable_encoder(response)


@order_router.get('/orders')
async def list_all_orders(db: db_session, Authorize: AuthJWT=Depends()):
    # protect the route
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid Token")
    
    current_user = Authorize.get_jwt_subject()

    user = db.query(User).filter(User.username==current_user).first()

    if user.is_staff:
        orders = db.query(Order).all()

        return jsonable_encoder(orders)
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="You are not a superuser")


@order_router.get('/orders/{id}')
async def get_order_by_id(id: int, db: db_session, Authorize: AuthJWT=Depends()):
    # protect the route
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid Token")
    
    user = Authorize.get_jwt_subject()

    current_user = db.query(User).filter(User.username==user).first()

    if current_user.is_staff:
        order = db.query(Order).filter(Order.id==id).first()

        return jsonable_encoder(order)
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="User not allowed to carry out request")


@order_router.get('/user/orders')
async def get_user_orders(db: db_session, Authorize: AuthJWT=Depends()):
    # protect the route
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid Token")
    
    user = Authorize.get_jwt_subject()

    current_user = db.query(User).filter(User.username==user).first()

    return jsonable_encoder(current_user.orders)


@order_router.get('/user/order/{order_id}', response_model=OrderModel)
async def get_specific_order(order_id: int, db: db_session, Authorize: AuthJWT=Depends()):
    # protect the route
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid Token")
    
    subject = Authorize.get_jwt_subject()

    current_user = db.query(User).filter(User.username==subject).first()

    orders = current_user.orders

    for o in orders:
        if o.id == order_id:
            return o

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="No order with such order id")