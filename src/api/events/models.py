# from pydantic import BaseModel, Field
from datetime import datetime,timezone 
from sqlmodel import SQLModel, Field
from typing import List, Optional
from timescaledb import TimescaleModel
import sqlmodel
from timescaledb.utils import get_utc_now

# page visits at any given time

class EventModel(TimescaleModel, table=True):
    # id: Optional[int] = Field(default=None, primary_key=True)
    page: str = Field(index=True) # /about, /contact, /pricing
    description: Optional[str] = ""
    # created_at: datetime = Field(
    #     default_factory=get_utc_now,
    #     sa_type=sqlmodel.DateTime(timezone=True),
    #     nullable=False
    # )
    updated_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlmodel.DateTime(timezone=True),
        nullable=False
    )

    __chunk_time_interval__ = "INTERVAL 1 day"
    __drop_after__ = "INTERVAL 3 months" # How many time to throw the whole X days hypertable to garbage.(Or store it...)

class EventCreateSchema(SQLModel):
    page: str
    description: Optional[str] = Field(default="")


class EventUpdateSchema(SQLModel):
    description: str


class EventListSchema(SQLModel):
    results: List[EventModel]
    count: int