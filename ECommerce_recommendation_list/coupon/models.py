from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from database import Base


class Coupon(Base):
    __tablename__= "coupon"

    id= Column(Integer, primary_key=True)
    code= Column(String(50),unique=True)
    valid_from= Column(DateTime)
    valid_to= Column(DateTime)
    discount= Column(Integer)
    active= Column(Boolean)

    order_coupon= relationship("Order", back_populates="coupon_related")