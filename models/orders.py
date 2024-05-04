from ..database import Base
from sqlalchemy import Column, Integer, Boolean, Text, String
from sqlalchemy_utils.types import ChoiceType


class Choice(Base):
    ORDER_STATUSES=(
        ('PENDING', 'pending'),
        ('IN-TRANSIT', 'in-transit'),
        ('DELIVERED', 'delivered')
    )

    __tablename__ = "orders"

    id = Column(Integer(max=10), primary_key=True, unique=True)
    quantity = Column(Integer, nullable=False)
    
