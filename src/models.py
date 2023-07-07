from sqlalchemy import String, Integer
from sqlalchemy.orm import (
    DeclarativeBase,
    mapped_column,
    Session,
)
from sqlalchemy import create_engine
from sqlalchemy.engine import URL


class Base(DeclarativeBase):
    pass


class Event(Base):
    __tablename__ = "Events"
    id = mapped_column(Integer, primary_key=True)
    timestamp = mapped_column(String(50))
    event = mapped_column(String(50))

    def __repr__(self):
        return (
            f"Event(id={self.id!r}, timestamp={self.timestamp!r}, event={self.event!r})"
        )


def create_session(database):
    url = URL.create(
        drivername="postgresql",
        username="postgres",
        password="postgres",
        host="postgres",
        database=database,
    )
    engine = create_engine(url, echo=True)
    Base.metadata.create_all(engine)
    session = Session(engine)
    return session
