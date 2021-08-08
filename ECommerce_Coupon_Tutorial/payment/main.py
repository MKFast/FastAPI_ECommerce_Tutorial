from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

from dependencies import env, templates, get_db
from orders.models import Order

router= APIRouter(
    prefix="/payment"
)

@router.get("/canceled")
def cancel_payment(request: Request):

    template= env.get_template("canceled.html")
    return templates.TemplateResponse(template, {"request": request})


@router.get("/done")
def cancel_payment(request: Request, db: Session= Depends(get_db)):

    order_id= request.session.get('order_id')
    order= db.query(Order).filter_by(id= order_id).first()
    order.is_paid= True
    db.commit()
    db.refresh(order)

    template= env.get_template("done.html")
    return templates.TemplateResponse(template, {"request": request})