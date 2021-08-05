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
    'orders/templates'
])
env= Environment(loader=loader)
templates=Jinja2Templates(directory="templates")
