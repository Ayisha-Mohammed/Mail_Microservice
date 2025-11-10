from sqlmodel import create_engine, Session, SQLModel
from app.core.config import settings
from app.db import models

engine = create_engine(settings.DATABASE_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session


def init_db():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    init_db()
