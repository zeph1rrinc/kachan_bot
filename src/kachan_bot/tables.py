from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Participant(Base):
    __tablename__ = 'participants'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=True)
    name = Column(String, nullable=True)
    rating = Column(Integer, default=0)
    current_question = Column(Integer, ForeignKey("questions.id"), nullable=True)


class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False)
    right_answer = Column(String, nullable=False)
    wrong_answer1 = Column(String, nullable=False)
    wrong_answer2 = Column(String, nullable=False)
    wrong_answer3 = Column(String, nullable=False)


question = relationship("Question", backref='participants')
