import sqlmodel
from .config import DATABASE_URL, DB_TIMEZONE
from sqlmodel import SQLModel, Session
import timescaledb

if DATABASE_URL == "":
    raise NotImplementedError("DATABASE_URL needs to be set")

engine = timescaledb.create_engine(DATABASE_URL, timezone=DB_TIMEZONE)

def init_db():
    print("creating database")
    SQLModel.metadata.create_all(engine)
    print("create hypertables")
    timescaledb.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session