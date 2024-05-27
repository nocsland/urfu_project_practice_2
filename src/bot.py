import os
import telebot
from telebot import types

api_key = os.getenv('BOT_API_KEY')
bot = telebot.TeleBot(api_key)


@bot.message_handler(commands=['start'])
def button_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Пополнить базу новой статьей")
    markup.add(item1)
    bot.send_message(message.chat.id, 'Задайте вопрос', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def text_reply(message):
    if message.text == "Пополнить базу новой статьей":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Задать вопрос")
        markup.add(item1)
        bot.send_message(message.chat.id, 'Отправьте документ',
                         reply_markup=markup)
    elif message.text == "Задать вопрос":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Пополнить базу новой статьей")
        markup.add(item1)
        bot.send_message(message.chat.id, 'Задайте вопрос',
                         reply_markup=markup)
    else:
        # Добавить код ответа на вопрос
        bot.send_message(message.chat.id, 'Тут должен быть ответ')


@bot.message_handler(content_types=['document'])
def document_reply(message):
    # Добавить код загрузки статьи
    bot.send_message(message.chat.id, 'Статья загружена в базу')


bot.infinity_polling()
