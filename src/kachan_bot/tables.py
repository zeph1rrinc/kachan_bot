from sqlalchemy import (
    Column,
    Integer,
    String
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Participant(Base):
    __tablename__ = 'participants'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=True)
    name = Column(String, nullable=True)
    rating = Column(Integer, default=0)

