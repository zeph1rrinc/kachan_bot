from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from random import shuffle
from loguru import logger

from .. import (
    tables,
    exceptions
)
from ..database import use_session, Session
from . import participants


def send_question(question: tables.Question, chat_id: int, bot: TeleBot):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    row = [
        KeyboardButton(question.right_answer),
        KeyboardButton(question.wrong_answer1),
        KeyboardButton(question.wrong_answer2),
        KeyboardButton(question.wrong_answer3)
    ]
    shuffle(row)
    keyboard.add(*row)
    keyboard.add(KeyboardButton("Закончить тест"))
    message_text = f"Вопрос №{question.id}\n{question.question}"
    msg = bot.send_message(chat_id, message_text, reply_markup=keyboard)
    bot.register_next_step_handler(msg, handle_answer, bot)


@use_session
def start_question(session: Session, user_id, bot: TeleBot):
    current_question = _get_current_question(session, user_id)
    if not current_question:
        raise exceptions.NotEnoughQuestionsError(chat_id=user_id,
                                                 message="К сожалению, вопросы кончились, попробуйте позже")
    send_question(current_question, user_id, bot)


def handle_answer(message, bot: TeleBot):
    session = Session()
    question = _get_current_question(session, message.from_user.id)
    participant = participants._get(session=session, chat_id=message.from_user.id, name='')
    answers = [
        question.right_answer,
        question.wrong_answer1,
        question.wrong_answer2,
        question.wrong_answer3,
        "Закончить тест"
    ]
    if message.text not in answers:
        session.close()
        bot.send_message(message.from_user.id, "Я тебя не понимаю, давай еще раз!")
        return send_question(question, message.from_user.id, bot)
    if message.text == "Закончить тест":
        return bot.send_message(message.from_user.id, "Окей!", reply_markup=ReplyKeyboardRemove())
    if message.text == question.right_answer:
        session.begin()
        setattr(participant, 'rating', participant.rating + 1)
        session.commit()
        bot.send_message(message.from_user.id, "Правильно! Следующий вопрос...")
    _update_question(session, question.id + 1, participant)
    new_question = _get_current_question(session, message.from_user.id)
    if not new_question:
        raise exceptions.NotEnoughQuestionsError(chat_id=message.from_user.id,
                                                 message="К сожалению, вопросы кончились, попробуйте позже")
    session.close()
    send_question(new_question, message.from_user.id, bot)


@use_session
def parse_file(session: Session, file: str, bot: TeleBot, chat_id: int):
    lines = file.split('\n')
    session.begin()
    for line in lines:
        question, answers = line.split(':')
        right_answer, wrong_answer1, wrong_answer2, wrong_answer3 = answers.strip().split('/')
        data = {
            "question": question,
            "right_answer": right_answer,
            "wrong_answer1": wrong_answer1,
            "wrong_answer2": wrong_answer2,
            "wrong_answer3": wrong_answer3,
        }
        if not _create_question(session=session, data=data):
            session.close()
            raise exceptions.CouldNotCreateQuestions(chat_id=chat_id, message="Произошла какая-то ошибка")
    session.commit()
    bot.send_message(chat_id, "Привет!")


def _create_question(session: Session, data: dict):
    try:
        question = tables.Question(**data)
        session.add(question)
        return question
    except Exception as _ex:
        logger.error(_ex)
        return False


def _update_question(session: Session, question_id: int, participant: tables.Participant):
    try:
        session.begin()
        setattr(participant, "current_question", question_id)
        session.commit()
        return True
    except Exception as _ex:
        logger.error(_ex)
        return False


def _get_current_question(session: Session, user_id: int):
    current_participant = participants._get(session=session, chat_id=user_id, name='')
    if not current_participant.current_question:
        _update_question(session, 1, current_participant)
    current_question = _get_question(session, id=current_participant.current_question)
    return current_question


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
