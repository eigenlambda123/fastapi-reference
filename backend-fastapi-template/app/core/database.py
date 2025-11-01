from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings

DB_URL = settings.DB_URL
print(f"Connecting to database: {DB_URL}")
connect_args = {"check_same_thread": False} if DB_URL.startswith("sqlite") else {}

engine = create_engine(DB_URL, echo=False, connect_args=connect_args)


def get_session():
    with Session(engine) as session:
        yield session


def init_db():
    # import app.models  # make sure your models are imported
    SQLModel.metadata.create_all(engine)
