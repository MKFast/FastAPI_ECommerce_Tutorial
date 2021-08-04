from slugify import slugify
from sqlalchemy import Boolean, TEXT, DECIMAL, Column, Integer, String, DateTime, ForeignKey
import datetime

from sqlalchemy.orm import relationship
from sqlalchemy_utils import URLType

from database import Base

class Category(Base):
    __tablename__ = "category"

    id= Column(Integer,primary_key=True)
    name=Column(String)
    slug= Column(String,unique=True)

    def __init__(self,*args,**kwargs):
        if not 'slug' in kwargs:
            kwargs['slug'] = slugify(kwargs.get('name',''))
        super(Category, self).__init__(*args,**kwargs)

    product_category= relationship("Product", back_populates="category_related")


class Product(Base):
    __tablename__ = "product"

    id= Column(Integer,primary_key=True)
    name= Column(String)
    description= Column(TEXT)
    url= Column(URLType)
    price= Column(DECIMAL(scale=2))
    available= Column(Boolean, default=True)
    created_date= Column(DateTime, default=datetime.datetime.utcnow)
    updated= Column(DateTime, onupdate=datetime.datetime.now)
    slug= Column(String,unique=True)

    def __init__(self,*args,**kwargs):
        if not 'slug' in kwargs:
            kwargs['slug'] = slugify(kwargs.get('name',''))
        super(Product, self).__init__(*args,**kwargs)

    category_id = Column(Integer, ForeignKey("category.id"))
    category_related= relationship("Category", back_populates= "product_category")

    product_order= relationship("OrderItem", back_populates="product_related")