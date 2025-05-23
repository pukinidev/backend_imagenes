from app.core.database import create_db_and_tables
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import api

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    
app = FastAPI(lifespan=lifespan)

app.include_router(api)
    
    

    
    

