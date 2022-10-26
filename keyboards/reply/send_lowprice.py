from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def request_send_lowprice() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(True, True)
    keyboard.add(KeyboardButton('Отправить запрос'))
    return keyboard


