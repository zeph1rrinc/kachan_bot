from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from .settings import settings
from .services import system, participants, tests

bot = TeleBot(settings.bot_token)


def filter_command(message, command):
    return message.text.lower().find(command) == 0


def parse_data(message):
    name, lastname, *_ = message.text.split(' ')[1:]
    username = _[0] if len(_) > 0 else ''
    return name, lastname, username


@bot.message_handler(commands=['start'])
@system.logging
def start(message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    row = [KeyboardButton("Да"), KeyboardButton("Нет")]
    keyboard.add(*row)
    msg = bot.send_message(message.from_user.id, 'Привет, ты студент?', reply_markup=keyboard)
    bot.register_next_step_handler(msg, participants.register_student, bot)


@bot.message_handler(func=lambda message: filter_command(message, "рейтинг"))
@system.logging
def get_rating(message):
    words = message.text.split()
    if len(words) == 1:
        return system.handle_get_players(message, ['name', 'rating'], bot)
    participant = participants.get(name=' '.join(words[1:]), chat_id=message.from_user.id)
    bot.send_message(message.from_user.id, f"{participant.name} - {participant.rating}")


@bot.message_handler(func=lambda message: filter_command(message, "участники"))
@system.logging
def get_participants(message):
    system.handle_get_players(message, ['name', 'username'], bot)


@bot.message_handler(func=lambda message: filter_command(message, "удалить"))
@system.logging
@system.check_admin
def delete_participant(message):
    name = ' '.join(message.text.split(' ')[1:])
    if participants.delete(name=name, chat_id=message.from_user.id):
        bot.send_message(message.from_user.id, f"Участник {name} успешно удален!")


@bot.message_handler(func=lambda message: filter_command(message, "обновить"))
@system.logging
@system.check_admin
def update_rating(message):
    *name, rating = message.text.split(' ')[1:]
    name = ' '.join(name)
    participant = participants.set_rating(name=name, rating=rating, chat_id=message.from_user.id)
    bot.send_message(message.from_user.id, f"Рейтинг участника {participant.name} успешно обновлен!")


@bot.message_handler(func=lambda message: filter_command(message, "сбросить рейтинг"))
@system.logging
@system.check_admin
def reset_rating(message):
    if participants.reset_rating():
        bot.send_message(message.from_user.id, "Рейтинг всех участников успешно сброшен")


@bot.message_handler(func=lambda message: filter_command(message, "очистить"))
@system.logging
@system.check_admin
def clear_participants(message):
    for participant in participants.get_all():
        participants.delete(name=participant.name, chat_id=message.from_user.id)
    bot.send_message(message.from_user.id, "Все участники успешно удалены")


@bot.message_handler(commands=['test'])
@system.logging
def start_test(message):
    tests.start_question(user_id=message.from_user.id, bot=bot)
