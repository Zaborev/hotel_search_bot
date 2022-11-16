from telebot.types import Message
from database import dbworker
from loader import bot
from states.cleart_history import ClearHistory


@bot.message_handler(commands=['clear_history'])
def history(message: Message) -> None:
    bot.delete_state(message.from_user.id, message.chat.id)
    bot.set_state(message.from_user.id, ClearHistory.first_state, message.chat.id)
    bot.send_message(message.from_user.id, f'⚠️История поиска будет удалена. Вы уверены? (Да/Нет)')


@bot.message_handler(state=ClearHistory.first_state)
def get_city(message: Message) -> None:
    if message.text in ('Да', 'да', 'Давай', 'ага', 'Ага'):
        try:
            dbworker.delete_tables('hotels', 'history', 'photos')
            bot.send_message(message.from_user.id, f'Хорошо. История удалена')
        except Exception:
            bot.send_message(message.from_user.id, f'⚠️Ошибка удаления истории поиска')

    elif message.text in ('Нет', 'нет', 'Не', 'не'):
        bot.send_message(message.from_user.id, f'Операция отменена.')
    else:
        bot.send_message(message.from_user.id, f'⚠️Введите Да или Нет')
