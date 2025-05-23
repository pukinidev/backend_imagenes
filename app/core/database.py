from typing import Generator
from sqlmodel import create_engine, Session, SQLModel
from app.dependencies import get_local_settings

local_settings = get_local_settings()
engine = create_engine(local_settings.db_url, echo=True, connect_args= {"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    
def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session