from fastapi import APIRouter, Request, Depends, Form,status
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from cart.cart import Cart
from dependencies import get_db, env, templates
from shop import models

router = APIRouter(
    prefix="/cart"
)

@router.get("/")
def cart_detail(request: Request,
                db: Session= Depends(get_db)):

    cart=Cart(request,db)

    template= env.get_template('cart.html')
    return templates.TemplateResponse(template,{"request": request,
                                                "cart": cart})

@router.post("/add")
def cart_add(request: Request,
             db: Session= Depends(get_db),
             id:int=Form(...),
             quantity: int= Form(...),
             update:bool=Form(...)):

    cart=Cart(request,db)
    product=db.query(models.Product).filter_by(id= id).first()
    cart.add(product=product,quantity=quantity,update_quantity=update)

    return RedirectResponse(url="/cart", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/remove/{id}")
def cart_remove(request:Request,
                id:int,
                db: Session=Depends(get_db)):

    cart= Cart(request,db)
    product=db.query(models.Product).filter_by(id=id).first()
    cart.remove(product)

    return RedirectResponse(url="/cart", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/remove_all")
def cart_remove_all(request:Request,
                    db: Session= Depends(get_db)):

    cart= Cart(request,db)
    cart.remove_all()

    return RedirectResponse(url="/cart", status_code=status.HTTP_303_SEE_OTHER)
