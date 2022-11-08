from loader import bot
from telebot.types import Message


@bot.message_handler(commands=['history'])
def lowprice(message: Message) -> None:
    bot.send_message(message.from_user.id,
                     f'Функция в разработке, попробуйте позднее!')
