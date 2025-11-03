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
    user_agent: Optional[str] = Field(default="", index=True)
    ip_address: Optional[str] = Field(default="", index=True)
    referrer: Optional[str] = Field(default="", index=True)
    session_id: Optional[str] = Field(default="", index=True)
    duration: Optional[int] = Field(default=0, index=True)
    __chunk_time_interval__ = "INTERVAL 1 day"
    __drop_after__ = "INTERVAL 3 months" # How many time to throw the whole X days hypertable to garbage.(Or store it...)

class EventCreateSchema(SQLModel):
    page: str
    user_agent: Optional[str] = Field(default="", index=True)
    ip_address: Optional[str] = Field(default="", index=True)
    referrer: Optional[str] = Field(default="", index=True)
    session_id: Optional[str] = Field(default="", index=True)
    duration: Optional[int] = Field(default=0, index=True)
    

# class EventUpdateSchema(SQLModel):
#     description: str


class EventListSchema(SQLModel):
    results: List[EventModel]
    count: int


class EventBucketSchema(SQLModel):
    bucket: datetime
    page: str
    ua: Optional[str] = ""
    operating_system: Optional[str] = ""
    avg_duration: Optional[float] = 0.0
    count: int