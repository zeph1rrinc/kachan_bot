from telebot import TeleBot

from .settings import settings
from .services import system, participants

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
    bot.send_message(message.from_user.id, 'Hello!')


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


@bot.message_handler(func=lambda message: filter_command(message, "создать"))
@system.logging
@system.check_admin
def create_participant(message):
    *name, username = parse_data(message)
    participant = participants.create(name=f"{' '.join(name)}", username=username)
    if participant:
        bot.send_message(message.from_user.id, f"Участник {participant.name} успешно создан!")


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
