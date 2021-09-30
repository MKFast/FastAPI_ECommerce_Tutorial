import redis
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

REDIS_HOST= 'localhost'
REDIS_PORT= 6379
REDIS_DB= 0

DATABASE_URL = "sqlite:///sql_db.db"

engine = create_engine(
    DATABASE_URL, connect_args= {"check_same_thread": False}
)

redis_database= redis.StrictRedis(host=REDIS_HOST,
                                  port=REDIS_PORT,
                                  db=REDIS_DB)

SessionLocal= sessionmaker(autocommit=False, bind=engine)

Base= declarative_base()

