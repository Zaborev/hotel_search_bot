from botrequests.hotels import request_city, request_list
from loader import bot
from states.lowprice import LowPriceState
from telebot.types import Message
from datetime import datetime


@bot.message_handler(commands=['lowprice'])
def lowprice(message: Message) -> None:
    bot.set_state(message.from_user.id, LowPriceState.city, message.chat.id)
    bot.send_message(message.from_user.id,
                     f'{message.from_user.full_name}, введите город для поиска выгодных предложений')


@bot.message_handler(state=LowPriceState.city)
def get_city(message: Message) -> None:
    bot.send_message(message.from_user.id, 'Ищу запрашиваемый Вами город...')
    r_city = request_city(message.text)[1]
    if r_city.lower() == message.text.lower():
        bot.send_message(message.from_user.id, 'Нашёл такой город в своем списке. Сколько отелей показать?')
        bot.set_state(message.from_user.id, LowPriceState.hotels_count, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['city'] = message.text
            data['city_id'] = r_city[0]
    else:
        bot.send_message(message.from_user.id, f'У меня в базе нет такого города. Повторите ввод.')


@bot.message_handler(state=LowPriceState.hotels_count)
def get_hotels_count(message: Message) -> None:
    if message.text.isdigit() and int(message.text) in range(1, 11):
        bot.send_message(message.from_user.id, 'Окей. Показать фото найденных отелей? (Да/Нет)')
        bot.set_state(message.from_user.id, LowPriceState.need_photo, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['hotels_count'] = message.text
    else:
        bot.send_message(message.from_user.id, f'Повторите ввод. Укажите количество отелей в выдаче (от 1 до 10)!')


@bot.message_handler(state=LowPriceState.need_photo)
def get_need_photo(message: Message) -> None:
    if message.text in ('Да', 'да', 'Давай', 'ага', 'Ага'):
        bot.send_message(message.from_user.id, 'Хорошо. Сколько фотографий для каждого отеля выбрать?')
        bot.set_state(message.from_user.id, LowPriceState.photo_count, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['need_photo'] = message.text
    elif message.text in ('Нет', 'нет', 'Неа', 'не', 'Не'):
        bot.set_state(message.from_user.id, LowPriceState.photo_count, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['need_photo'] = message.text
            data['photo_count'] = 0
            text = f'Спасибо, ищем подходящие отели по следующему запросу:\n' \
                   f'Город: {data["city"]}\n' \
                   f'Сколько отелей показывать: {data["hotels_count"]}\n' \
                   f'Показывать фото отелей: {data["need_photo"]}\n' \
                   f'Сколько фото показывать: {data["photo_count"]}\n'
            bot.send_message(message.from_user.id, text)
            current_day = datetime.now().date()
            parameters = [data["city"], str(current_day), str(current_day), '1', '50', message.from_user.full_name,
                          '/lowprice', '0', '100000', '20.0']
            results = (request_list(request_city(data["city"])[0], list_param=parameters))
            data['results'] = results
            for show in range(data["hotels_count"]):
                print_info_about_hotel = f'{show+1}. {results[2]}\n' \
                                         f'Адрес: {results[3]}\n' \
                                         f'До центра города: {results[4]}\n' \
                                         f'Цена за сутки: {results[5]}\n' \
                                         f'Рейтинг: {results[8]}'
                bot.send_message(message.from_user.id, print_info_about_hotel)

    else:
        bot.send_message(message.from_user.id, f'Не понял. Нужны фото отелей? Введите Да/Нет')


@bot.message_handler(state=LowPriceState.photo_count)
def get_photo_count(message: Message) -> None:
    if int(message.text) in range(1, 11):
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['photo_count'] = message.text
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            text = f'Спасибо, ищем подходящие отели по следующему запросу:\n' \
                   f'Город: {data["city"]}\n' \
                   f'Сколько отелей показывать: {data["hotels_count"]}\n' \
                   f'Показывать фото отелей: {data["need_photo"]}\n' \
                   f'Сколько фото показывать: {data["photo_count"]}\n'
            bot.send_message(message.from_user.id, text)
    else:
        bot.send_message(message.from_user.id, 'Sorry, могу показать только от 1 до 10 фоток отеля...')
