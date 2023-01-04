from loguru import logger
from sqlalchemy import or_

from .. import (
    tables,
    exceptions
)
from ..database import use_session, Session


@use_session
def get_all(session) -> list:
    return _get_many(session)


@use_session
def create(session: Session, name: str, username: str = ''):
    try:
        participant = tables.Participant(name=name, username=username)
        session.begin()
        session.add(participant)
        session.commit()
        return participant
    except Exception as _ex:
        logger.error(_ex)
        return False


@use_session
def get(session: Session, name: str, chat_id: int):
    return _get(session, name, chat_id)


@use_session
def delete(session: Session, name: str, chat_id: int):
    participant = _get(session, name, chat_id)
    session.begin()
    session.delete(participant)
    session.commit()
    return True


@use_session
def set_rating(session: Session, name: str, rating: int, chat_id: int):
    participant = _get(session, name, chat_id)
    session.begin()
    setattr(participant, "rating", rating)
    session.commit()
    return participant


@use_session
def reset_rating(session: Session):
    participants = _get_many(session)
    session.begin()
    for participant in participants:
        setattr(participant, "rating", 0)
    session.commit()
    return True

def _get(session: Session, name: str, chat_id: int):
    participant = (
        session
            .query(tables.Participant)
            .filter(or_(tables.Participant.name == name, tables.Participant.username == name))
            .first()
    )
    if not participant:
        raise exceptions.NonExistentParticipantError(chat_id=chat_id, message="Участника не существует!")
    return participant


def _get_many(session):
    participants = (
        session
            .query(tables.Participant)
            .order_by(tables.Participant.rating.desc())
            .all()
    )
    return participants
