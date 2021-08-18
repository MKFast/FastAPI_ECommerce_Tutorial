from fastapi import APIRouter, Request, Depends, Form,status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from cart.cart import Cart
from dependencies import get_db, env, templates
from shop import models
from shop.recommender import Recommender

router = APIRouter(
    prefix="/cart"
)

@router.get("/")
def cart_detail(request: Request,
                db: Session= Depends(get_db)):

    cart=Cart(request,db)

    recommender = Recommender()
    cart_products= list(jsonable_encoder([item['product'] for item in cart]))
    if cart_products:
        recommended_products= recommender.suggest_products_for(db,cart_products,max_result=4)
    else:
        recommended_products= None

    template= env.get_template('cart.html')
    return templates.TemplateResponse(template,{"request": request,
                                                "cart": cart,
                                                "recommended_products": recommended_products})

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
