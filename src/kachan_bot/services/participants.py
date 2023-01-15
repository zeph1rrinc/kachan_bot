from loguru import logger
from sqlalchemy import or_
from telebot import TeleBot
from telebot.types import ReplyKeyboardRemove

from .. import (
    tables,
    exceptions
)
from ..database import use_session, Session


@use_session
def get_all(session) -> list:
    return _get_many(session)


@use_session
def create(session: Session, name: str, username: str = '', id: int = None):
    try:
        data = {"name": name, "username": username}
        if id:
            data["id"] = id
        participant = tables.Participant(**data)
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
            .filter(
            or_(
                tables.Participant.name == name,
                tables.Participant.username == name,
                tables.Participant.id == chat_id
            ))
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


def register_student(message, bot: TeleBot):
    chat_id = message.from_user.id
    empty_keyboard = ReplyKeyboardRemove()
    match message.text.lower():
        case "нет":
            bot.send_message(chat_id, "Окей!", reply_markup=empty_keyboard)
        case "да":
            data = {
                "name": message.from_user.first_name,
                "username": message.from_user.username,
                "id": chat_id
            }
            if message.from_user.last_name:
                data["name"] += f" {message.from_user.last_name}"
            participant = create(**data)
            if not participant:
                raise exceptions.BaseBotError(chat_id=chat_id, message="Какая-то ошибка")
            bot.send_message(chat_id, "Ты успешно зарегистрирован!", reply_markup=empty_keyboard)
        case _:
            msg = bot.send_message(chat_id, "Не понял. Ты студент?")
            bot.register_next_step_handler(msg, register_student, bot)
