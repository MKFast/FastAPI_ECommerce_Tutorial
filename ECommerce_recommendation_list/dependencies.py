import stripe
from jinja2 import FileSystemLoader, Environment
from starlette.templating import Jinja2Templates

from database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

loader = FileSystemLoader([
    'templates/',
    'shop/templates',
    'cart/templates',
    'orders/templates',
    'payment/templates'
])
env= Environment(loader=loader)
templates=Jinja2Templates(directory="templates")

stripe.api_key= 'sk_test_51JLoYhHjy4UHtREduvNTeCRc2jrJ7BHS6rxV3JtFiXgm2hRsVt2kIz4NYOyrMwVX1bIAzyV8V8n4RVy0MPhmPT1B00yXFyYC5Z'