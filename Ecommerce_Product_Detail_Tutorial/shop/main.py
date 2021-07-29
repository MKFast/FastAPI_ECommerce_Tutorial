from fastapi import FastAPI, Request, Depends, APIRouter
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from dependencies import get_db, templates, env
from shop import crud
from shop.models import Category

router = APIRouter(
    prefix="/product"
)

@router.get("/{category_slug}")
def product_list(request:Request,category_slug:str, db:Session = Depends(get_db),
                 page: int=1):
    products= crud.product_list(db=db,
                                category_slug=category_slug)[16*(page-1):16*(page)]
    categories= db.query(Category).all()
    category= db.query(Category).filter_by(slug=category_slug).first()

    template= env.get_template('list.html')

    return templates.TemplateResponse(template,{"request": request,
                                                   "page": page,
                                                   "products": jsonable_encoder(products),
                                                   "category":jsonable_encoder(category),
                                                   "categories":jsonable_encoder(categories)})


@router.get("/")
def product_list(request:Request,category_slug:str=None, db:Session = Depends(get_db),
                 page: int=1):
    products= crud.product_list(db=db,
                                category_slug=category_slug)[16*(page-1):16*(page)]
    categories= db.query(Category).all()
    category= db.query(Category).filter_by(slug=category_slug).first()

    template= env.get_template('list.html')

    return templates.TemplateResponse(template,{"request": request,
                                                   "page": page,
                                                   "products": jsonable_encoder(products),
                                                   "category":jsonable_encoder(category),
                                                   "categories":jsonable_encoder(categories)})
