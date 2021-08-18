import datetime

from fastapi import APIRouter, Request, Depends, Form,status
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from coupon.models import Coupon
from dependencies import get_db

router= APIRouter(
    prefix='/coupon'
)

@router.post("/apply")
def coupon_apply(request: Request, db: Session= Depends(get_db),
                 code: str= Form(...)):
    now= datetime.datetime.now()

    try:
        coupon= db.query(Coupon).filter(Coupon.code == code,
                                        Coupon.valid_from.__le__(now),
                                        Coupon.valid_to.__ge__(now),
                                        Coupon.active== True).first()

        request.session['coupon_id'] = coupon.id

    except:
        request.session['coupon_id']= None

    return RedirectResponse(url="/cart", status_code=status.HTTP_303_SEE_OTHER)
