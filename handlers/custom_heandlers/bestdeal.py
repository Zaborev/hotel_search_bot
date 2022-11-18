from datetime import date, timedelta

from telegram_bot_calendar import DetailedTelegramCalendar

from botrequests.hotels import request_city, request_list, request_photo
from loader import bot
from states.bestdeal import BestDealState
from telebot.types import Message
from keyboards.reply.photo_mediagroup import create_media_group
from database import dbworker
from config_data import config

command = '/bestdeal'


@bot.message_handler(commands=['bestdeal'])
def bestdeal(message: Message) -> None:
    bot.delete_state(message.from_user.id, message.chat.id)
    bot.set_state(message.from_user.id, BestDealState.city, message.chat.id)
    bot.send_message(message.from_user.id,
                     f'{message.from_user.full_name}, введите город для поиска отелей с диапазоном цен '
                     f'(на русском языке)')


@bot.message_handler(state=BestDealState.city)
def get_city(message: Message) -> None:
    if message.text.isalpha():
        bot.send_message(message.from_user.id, 'Ищу запрашиваемый Вами город в своей базе...')
        r_city = request_city(message.text)[1]
        if r_city.lower() == message.text.lower():
            bot.send_message(message.from_user.id, 'Город найден.')
            calendar, step = DetailedTelegramCalendar(locale='ru', min_date=date.today()).build()
            bot.send_message(message.chat.id, f"Введите дату заезда", reply_markup=calendar)
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['city'] = message.text
        else:
            bot.send_message(message.from_user.id, f'⚠️У меня в базе нет такого города. Повторите ввод.')
        bot.set_state(message.from_user.id, BestDealState.hotels_count, message.from_user.id)
    else:
        bot.send_message(message.from_user.id, f'⚠️Название города может содержать только буквы! Повторите ввод.')


@bot.message_handler(state=BestDealState.hotels_count)
def get_hotels_count(message: Message) -> None:
    if message.text.isdigit() and int(message.text) in range(1, 11):
        bot.send_message(message.from_user.id, 'Окей. Задайте минимальную стоимость суток проживания в отеле:')
        bot.set_state(message.from_user.id, BestDealState.price_min, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['hotels_count'] = message.text
    else:
        bot.send_message(message.from_user.id, f'Повторите ввод. Укажите количество отелей в выдаче (от 1 до 10)!')


@bot.message_handler(state=BestDealState.price_min)
def get_price_min(message: Message) -> None:
    if message.text.isdigit() and int(message.text) > 0:
        bot.send_message(message.from_user.id, 'Хорошо, запомнил. Переходим к следующему пункту. Задайте максимальную'
                                               ' суточную стоимость отеля:')
        bot.set_state(message.from_user.id, BestDealState.price_max, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['price_min'] = message.text
    else:
        bot.send_message(message.from_user.id, f'Максимальная стоимость суток проживания в отеле '
                                               f'должна состоять из цифр и быть больше 0')


@bot.message_handler(state=BestDealState.price_max)
def get_price_max(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if message.text.isdigit() and int(message.text) > int(data["price_min"]):
            bot.send_message(message.from_user.id, 'ОК, запомнил. Введите максимальное расстояние до центра '
                                                   '(Например 10)')
            bot.set_state(message.from_user.id, BestDealState.distance, message.chat.id)
            data['price_max'] = message.text
        else:
            bot.send_message(message.from_user.id, f'Максимальная стоимость суток проживания в отеле '
                                                   f'должна состоять из цифр и быть больше минимальной '
                                                   f'стоимости суток проживания в отеле')


@bot.message_handler(state=BestDealState.distance)
def get_price_max(message: Message) -> None:
    if message.text.isdigit() and float(message.text) > 0:
        bot.send_message(message.from_user.id, 'ОК, запомнил. Показать фото отелей?')
        bot.set_state(message.from_user.id, BestDealState.need_photo, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['distance'] = message.text
    else:
        bot.send_message(message.from_user.id, f'Расстояние от центра города до отеля'
                                               f'должно состоять из цифр и быть больше 0')


@bot.message_handler(state=BestDealState.need_photo)
def get_need_photo(message: Message) -> None:
    if message.text in ('Да', 'да', 'Давай', 'ага', 'Ага'):
        bot.send_message(message.from_user.id, 'Хорошо. Сколько фотографий для каждого отеля выбрать?')
        bot.set_state(message.from_user.id, BestDealState.photo_count, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['need_photo'] = message.text
    elif message.text in ('Нет', 'нет', 'Неа', 'не', 'Не'):
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['need_photo'] = message.text
            data['photo_count'] = 0
            city, start_date, end_date, hotels_count, photo_count = data["city"], data["start_date"], \
                                                                    data["end_date"], data["hotels_count"], \
                                                                    data['photo_count']
            price_min, price_max, distance = data["price_min"], data["price_max"], data["distance"]
            text = f'Спасибо, ищем подходящие отели по следующему запросу:\n' \
                   f'Город: {city}\n' \
                   f'Даты проживания: {start_date} - {end_date}\n' \
                   f'Диапазон цен за сутки: {price_min} - {price_max}\n руб.' \
                   f'Расстояние до центра города: {distance}\n' \
                   f'Сколько отелей показывать: {hotels_count}\n' \
                   f'Показывать фото отелей: {data["need_photo"]}\n' \
                   f'Сколько фото показывать: {photo_count}\n'
            bot.send_message(message.from_user.id, text)
        parameters = [city, start_date, end_date, config.people_count,
                      hotels_count, message.chat.id, command, price_min, price_max, distance]
        results = (request_list(request_city(city)[0], list_param=parameters))
        if len(results) >= int(hotels_count):
            history = (
                str(message.chat.id), str(message.chat.id), str(config.date_and_time), city,
                start_date, end_date, hotels_count, photo_count, False,
                command, price_min, price_max, distance)
            if dbworker.set_history(history=history):
                dbworker.set_hotels(hotels=tuple(results))
            for show in range(int(hotels_count)):
                print_info_about_hotel = f'🏨 {show + 1}. {results[show][2]}\n' \
                                         f'🌎 Адрес: {results[show][3]}\n' \
                                         f'🌐 Сайт: https://www.hotels.com/ho{results[show][1]}/\n' \
                                         f'↔ До центра города: {results[show][4]}\n' \
                                         f'💳 Цена за сутки: {results[show][5]} руб.\n' \
                                         f'⭐ Рейтинг пользователей: {results[show][6]}'
                bot.send_message(message.from_user.id, print_info_about_hotel, disable_web_page_preview=True)
        else:
            bot.send_message(message.from_user.id, f'⚠️Нет результатов поиска с заданными параметрами.'
                                                   f' Повторите запрос.')
        bot.delete_state(message.from_user.id, message.chat.id)
    else:
        bot.send_message(message.from_user.id, f'⚠️Не понял. Нужны фото отелей? Введите Да/Нет')


@bot.message_handler(state=BestDealState.photo_count)
def get_photo_count(message: Message) -> None:
    if int(message.text) in range(1, 6):
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['photo_count'] = message.text
            city, start_date, end_date, hotels_count, photo_count = data["city"], data["start_date"], \
                                                                    data["end_date"], data["hotels_count"], \
                                                                    data['photo_count']
            price_min, price_max, distance = data["price_min"], data["price_max"], data["distance"]
            text = f'Спасибо, ищем подходящие отели по следующему запросу:\n' \
                   f'Город: {city}\n' \
                   f'Даты проживания: {start_date} - {end_date}\n' \
                   f'Диапазон цен за сутки: {price_min} - {price_max}\n' \
                   f'Расстояние до центра города: {distance}\n' \
                   f'Сколько отелей показывать: {hotels_count}\n' \
                   f'Показывать фото отелей: {data["need_photo"]}\n' \
                   f'Сколько фото показывать: {photo_count}\n'
            bot.send_message(message.from_user.id, text)

        parameters = [city, start_date, end_date, config.people_count,
                      hotels_count, message.chat.id, command, price_min, price_max, distance]
        results = (request_list(request_city(city)[0], list_param=parameters))
        if len(results) >= int(hotels_count):
            history = (
                str(message.chat.id), str(message.chat.id), str(config.date_and_time), city, start_date, end_date,
                hotels_count, photo_count, False, command, price_min, price_max, distance)
            if dbworker.set_history(history=history):
                dbworker.set_hotels(hotels=tuple(results))
            for show in range(int(hotels_count)):
                print_info_about_hotel = f'🏨 {show + 1}. {results[show][2]}\n' \
                                         f'🌎 Адрес: {results[show][3]}\n' \
                                         f'🌐 Сайт: https://www.hotels.com/ho{results[show][1]}/\n' \
                                         f'↔ До центра города: {results[show][4]}\n' \
                                         f'💳 Цена за сутки: {results[show][5]} руб.\n' \
                                         f'⭐ Рейтинг пользователей: {results[show][6]}\n' \

                bot.send_message(message.from_user.id, print_info_about_hotel, disable_web_page_preview=True)
                photos = request_photo(results[show][1])
                dbworker.set_photos(photos=tuple(photos))
                if photos:
                    media = create_media_group(photos, int(photo_count))
                    if len(media) != 0:
                        try:
                            bot.send_media_group(chat_id=message.chat.id, media=media)
                        except:
                            media = create_media_group(photos, int(photo_count))
                            if len(media) != 0:
                                bot.send_media_group(chat_id=message.chat.id, media=media)
                            else:
                                bot.send_message(chat_id=message.chat.id, text='⚠️Фотографии не найдены')
                else:
                    bot.send_message(message.from_user.id, text='⚠️Фотографии не найдены')
        else:
            bot.send_message(message.from_user.id, f'⚠️Нет результатов поиска с заданными параметрами.'
                                                   f' Повторите запрос.')
        bot.delete_state(message.from_user.id, message.chat.id)
    else:
        bot.send_message(message.from_user.id, '⚠️Sorry, могу показать только от 1 до 5 фоток отеля...')