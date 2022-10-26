from loader import bot
from telebot.types import Message


@bot.message_handler(commands=['hello_world'])
def lowprice(message: Message) -> None:
    bot.send_message(message.from_user.id,
                     f'Привет, {message.from_user.full_name}, рад знакомству!')
