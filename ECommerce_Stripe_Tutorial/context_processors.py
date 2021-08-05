import jinja2
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from starlette_context.middleware import ContextMiddleware

from cart.cart import Cart
from dependencies import get_db


class CartMiddleware(ContextMiddleware):

    @jinja2.pass_context
    def cart(context: dict,db: Session = Depends(get_db)):
        request= context["request"]
        return jsonable_encoder(Cart(request,db))

        