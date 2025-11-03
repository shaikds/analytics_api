from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.events import router as event_router
from api.events.models import EventModel
from contextlib import asynccontextmanager
from api.db.session import init_db



@asynccontextmanager
async def lifespan(app: FastAPI):
    # before app startup
    
    init_db()
    yield 
    # clean up

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    # TODO: Should be changed before going to production.
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(event_router, prefix ='/api/events')

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/health")
def read_api_health():
    return {"status": "ok"}
