from fastapi.encoders import jsonable_encoder

from database import redis_database
from shop.models import Product


class Recommender(object):
    def get_product_key(self, id):
        return 'product:{}:ordered_with'.format(id)

    def products_bought(self, products):
        product_ids= [p.id for p in products]
        for product_id in product_ids:
            for with_id in product_ids:
                if product_id != with_id:
                    redis_database.zincrby(self.get_product_key(product_id),
                                           1,with_id)

    def suggest_products_for(self,db,products, max_result=6):
        product_ids= [p["id"] for p in products]

        if len(products) == 1:
            suggestions= redis_database.zrange(
                self.get_product_key(product_ids[0]),
                0, -1, desc=True
            )[:max_result]

        else:
            flat_ids= ''.join([str(id) for id in product_ids])
            tmp_key= 'tmp_{}'.format(flat_ids)
            keys= [self.get_product_key(id) for id in product_ids]
            redis_database.zunionstore(tmp_key, keys)
            redis_database.zrem(tmp_key, *product_ids)

            suggestions= redis_database.zrange(tmp_key,0,-1,desc=True)[:max_result]

            redis_database.delete(tmp_key)

        suggested_product_ids= [int(id) for id in suggestions]
        suggested_products= list(jsonable_encoder(db.query(Product).filter(
            Product.id.in_(suggested_product_ids)
        ).all()))

        suggested_products.sort(key=lambda x: suggested_product_ids.index(x["id"]))

        return suggested_products