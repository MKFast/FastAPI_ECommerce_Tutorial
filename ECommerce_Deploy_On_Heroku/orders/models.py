import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType

from database import Base


class Order(Base):
    __tablename__= "orders"

    id= Column(Integer, primary_key=True)
    first_name= Column(String)
    last_name= Column(String)
    email= Column(EmailType)
    address= Column(String)
    postal_code= Column(String)
    city=Column(String)
    created_date= Column(DateTime, default=datetime.datetime.utcnow)
    is_paid= Column(Boolean, default=False)

    order_item= relationship("OrderItem", back_populates="order_related")

    coupon_id= Column(Integer, ForeignKey("coupon.id"), nullable=True)
    coupon_related= relationship("Coupon", back_populates= "order_coupon")
    discount= Column(Integer)

    def get_total_cost(self):
        total_cost= sum(item.get_cost() for item in self.items.all())
        return total_cost

class OrderItem(Base):
    __tablename__= "orderitem"

    id= Column(Integer,primary_key=True)
    price= Column(DECIMAL(scale=2))
    quantity= Column(Integer, default=1)

    product_id= Column(Integer, ForeignKey("product.id"))
    product_related= relationship("Product", back_populates="product_order")

    order_id= Column(Integer, ForeignKey("orders.id"))
    order_related= relationship("Order",back_populates="order_item")

    def get_cost(self):
        return self.price * self.quantity