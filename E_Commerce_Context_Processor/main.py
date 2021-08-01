from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles

import shop
import cart
from database import engine
from shop import main, models
from cart import main

secret_key='cart'

middleware = [
    Middleware(SessionMiddleware,secret_key=secret_key)
]

app = FastAPI(middleware=middleware)

app.mount("/static",StaticFiles(directory="static"), name="static")

shop.models.Base.metadata.create_all(bind=engine)

app.include_router(shop.main.router)
app.include_router(cart.main.router)
