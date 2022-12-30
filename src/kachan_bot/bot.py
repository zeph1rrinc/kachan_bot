from telebot import TeleBot

from .settings import settings

bot = TeleBot(settings.bot_token)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, 'Hello!')
    

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.send_message(message.from_user.id, message.text)
