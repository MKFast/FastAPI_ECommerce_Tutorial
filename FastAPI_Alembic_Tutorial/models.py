from sqlalchemy import  Column,String,TEXT,Integer

from database import Base

class Shop(Base):
    __tablename__="shop"

    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    description = Column(TEXT)
    price = Column(Integer)
