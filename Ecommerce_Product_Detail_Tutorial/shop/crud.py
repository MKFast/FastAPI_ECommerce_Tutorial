from fastapi import Depends
from sqlalchemy.orm import Session

from dependencies import get_db
from shop import models


def product_list(db:Session= Depends(get_db), category_slug: str=None):

    if category_slug:
        category_related= db.query(models.Category).filter_by(slug=category_slug).first()
        return db.query(models.Product).filter_by(category_related= category_related).all()

    return db.query(models.Product).all()

