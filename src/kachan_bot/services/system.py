from loguru import logger
from json import dumps
from telebot.types import Message
from telebot import TeleBot

from . import participants
from ..settings import settings
from ..exceptions import NotAdminError


def check_admin(func):
    def _wrapper(message, *args, **kwargs):
        admins = settings.admin_chats.split(',')
        is_admin = False
        for admin in admins:
            if str(message.from_user.id) == admin:
                is_admin = True
        if not is_admin:
            raise NotAdminError(chat_id=message.from_user.id, message="Недостаточно прав для выполнения этого действия")
        func(message, *args, **kwargs)

    return _wrapper


def logging(func):
    def _wrapper(message, *args, **kwargs):
        data = {
            "user": {
                "id": message.from_user.id,
                "name": f"{message.from_user.first_name} {message.from_user.last_name}",
                "username": message.from_user.username
            },
            "content_type": message.content_type,
            "text": message.text
        }
        logger.debug(f"Received new message - {dumps(data, ensure_ascii=False)}")
        func(message, *args, **kwargs)

    return _wrapper


def handle_get_players(message: Message, fields: list, bot: TeleBot):
    answer = ''
    players = participants.get_all()
    if not players:
        return bot.send_message(message.from_user.id, "Еще нет игроков")
    for player in players:
        index = players.index(player) + 1
        answer += f"{index}. "
        for field in fields:
            value = player.__dict__[field]
            if fields.index(field) == 0:
                answer += f"{value}"
            else:
                if value or (type(value) == int and value == 0):
                    answer += f" - {value}"
        answer = answer.strip() + '\n'
    bot.send_message(message.from_user.id, answer)