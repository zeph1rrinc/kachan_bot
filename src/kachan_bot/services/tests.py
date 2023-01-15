from telebot import TeleBot

from .. import (
    tables,
    exceptions
)
from ..database import use_session, Session
from . import participants


@use_session
def start_question(session: Session, user_id, bot: TeleBot):
    current_participant = participants._get(session=session, chat_id=user_id, name='')
    print(current_participant.name)
    current_question = _get_question(session, id=current_participant.current_question)
    print(current_question)


def _get_question(session: Session, id: int):
    question = (
        session
            .query(tables.Question)
            .filter(tables.Question.id == id)
            .first()
    )
    if not question:
        return False
    return question
