from telebot.types import Message
import random

from loader import bot


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@bot.message_handler(state=None)
def bot_echo(message: Message):
    hi = ('Привет', 'привет', 'здравствуйте', 'Здорово', 'хай', 'Хай')
    replicas = ('Привет, чем я могу Вам помочь?', 'Добрый день, давайте я помогу Вам подобрать отель?',
                'Добрый день, готов услышать ваш вопрос!',
                'Привет, сегодня отличный день, чтобы отправиться в поездку! Начнём подбирать отель?')
    if message.text in hi:
        random_replica = random.randint(0, len(replicas))
        bot.send_message(message.from_user.id, replicas[random_replica])
    else:
        bot.send_message(message.from_user.id, "Я Вас не понимаю. Напишите /help чтобы узнать список команд")
