from keyboards.reply.send_lowprice import request_send_lowprice
from loader import bot
from states.lowprice import LowPriceState
from telebot.types import Message


@bot.message_handler(commands=['lowprice'])
def lowprice(message: Message) -> None:
    bot.set_state(message.from_user.id, LowPriceState.city, message.chat.id)
    bot.send_message(message.from_user.id,
                     f'{message.from_user.username}, введите город для поиска выгодных предложений')


@bot.message_handler(state=LowPriceState.city)
def get_city(message: Message) -> None:
    if message.text.isalpha():
        bot.send_message(message.from_user.id, 'Спасибо, запомнил. Сколько отелей показать?')
        bot.set_state(message.from_user.id, LowPriceState.hotels_count, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['city'] = message.text
    else:
        bot.send_message(message.from_user.id, f'Повторите ввод. Название города должно содержать только буквы!')


@bot.message_handler(state=LowPriceState.hotels_count)
def get_hotels_count(message: Message) -> None:
    if message.text.isdigit() and int(message.text) in range(1, 21):
        bot.send_message(message.from_user.id, 'Спасибо, запомнил. Показать фото найденных отелей? (Да/Нет)')
        bot.set_state(message.from_user.id, LowPriceState.need_photo, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['hotels_count'] = message.text
    else:
        bot.send_message(message.from_user.id, f'Повторите ввод. Укажите количество отелей в выдаче (от 1 до 20)!')


@bot.message_handler(state=LowPriceState.need_photo)
def get_need_photo(message: Message) -> None:
    if message.text in ('Да', 'да', 'Давай', 'ага', 'Ага'):
        bot.send_message(message.from_user.id, 'Хорошо. Сколько фотографий для каждого отеля выбрать?')
        bot.set_state(message.from_user.id, LowPriceState.photo_count, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['need_photo'] = message.text
    elif message.text in ('Нет', 'нет', 'Неа', 'не', 'Не'):
        bot.send_message(message.from_user.id, 'Не надо, так не надо :) Нажми на кнопку, чтобы отправить запрос',
                         reply_markup=request_send_lowprice())
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['photo_count'] = 0
    else:
        bot.send_message(message.from_user.id, f'Не понял. Показать фото отелей?')


@bot.message_handler(state=LowPriceState.photo_count)
def get_photo_count(message: Message) -> None:
    if int(message.text) in range(1, 21):
        bot.send_message(message.from_user.id, 'Окей, нажмите на кнопку, чтобы отправить запрос.',
                         reply_markup=request_send_lowprice())
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['photo_count'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Sorry, могу показать только от 1 до 20 фоток отеля...')


@bot.message_handler(content_types=['text', 'send_lowprice'], state=LowPriceState.photo_count)
def get_lowprice(message: Message) -> None:
    if message.content_type == 'send_lowprice':
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            text = f'Спасибо, ищем подходящие отели по следующему запросу:\n' \
                   f'Город: {data["city"]}\n' \
                   f'Сколько отелей показывать: {data["hotel_count"]}\n' \
                   f'Показывать фото отелей: {data["need_photo"]}\n' \
                   f'Сколько фото показывать: {data["photo_count"]}\n'
            bot.send_message(message.from_user.id, text)
    else:
        bot.send_message(message.from_user.id, 'Чтобы отправить запрос, нажмите на кнопку')
