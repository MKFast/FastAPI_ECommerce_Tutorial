from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

import shop
from database import engine
from shop import main, models

app = FastAPI()

app.mount("/static",StaticFiles(directory="static"), name="static")

shop.models.Base.metadata.create_all(bind=engine)

app.include_router(shop.main.router)

