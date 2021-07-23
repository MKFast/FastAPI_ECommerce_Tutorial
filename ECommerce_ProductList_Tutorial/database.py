from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "sqlit://./sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args= {"check_same_thread": False}
)

sessionLocal= sessionmaker(autocommit=False, bin=engine)

Base= declarative_base()