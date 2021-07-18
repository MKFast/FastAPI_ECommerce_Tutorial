from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import crud
import models
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/create/")
def create_product(title:str,description:str,price:int,db: Session = Depends(get_db)):
    return crud.create_product(title=title,description=description,price=price,db=db)

@app.get("/list/")
def product_list(db: Session = Depends(get_db)):
    return crud.product_list(db=db)
