from fastapi.encoders import jsonable_encoder

from coupon.models import Coupon
from shop.models import Product

secret_key= 'cart'

class Cart(object):

    def __init__(self,request, db):
        self.session= request.session
        self.db=db
        cart= self.session.get(secret_key)

        if not cart:
            cart = self.session[secret_key]= {}

        self.cart=cart

        self.coupon_id= self.session.get('coupon_id')

    def add(self,product, quantity=1,update_quantity=False):
        product_id=str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)
                                     }

        if update_quantity:
            self.cart[product_id]['quantity']= quantity
        else:
            self.cart[product_id]['quantity'] += quantity

    def remove(self,product):
        product_id= str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]

    def remove_all(self):
        product_ids= list(self.cart.keys())

        for id in product_ids:
            del self.cart[str(id)]

    def __iter__(self):
        product_ids = list(self.cart.keys())
        products= self.db.query(Product).filter(
            Product.id.in_(product_ids)
        ).all()
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = jsonable_encoder(product)

        for item in cart.values():
            item['total_price'] = float((item['price']))* float(item['quantity'])

            yield item

    def __len__(self):
        return sum((item['price'])*item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(float(item['price'])*float(item['quantity']) for item in self.cart.values())

    @property
    def coupon(self):
        if self.coupon_id:
            return self.db.query(Coupon).filter(Coupon.id == self.coupon_id).first()
        return None

    def get_discount(self):
        if self.coupon:
            return float("{:.2f}".format((self.coupon.discount / float(100))* self.get_total_price()))

        return float("{:.2f}".format(0))

    def get_total_price_after_discount(self):
        return float("{:.2f}".format(self.get_total_price()-self.get_discount()))
