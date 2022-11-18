from telebot.types import Message
from database import dbworker
from loader import bot


@bot.message_handler(commands=['history'])
def history(message: Message) -> None:
    history = dbworker.get_history(id=str(message.chat.id))
    if history:
        for record in history:
            error = record[10]
            uid = record[0]
            string = f'➡️Дата и время запроса: {record[1]}' \
                     f'\n➡️Команда: {record[2]}' \
                     f'\n➡️Город: {record[3]}' \
                     f'\n➡️Количество отелей для поиска: {record[4]}' \
                     f'\n➡️Максимальное расстояние от центра: {record[9]} км'
            if record[2] == '/bestdeal':
                string += f'\n🔜 Дата заезда: {record[5]}' \
                          f'\n🔙 Дата выезда: {record[6]}' \
                          f'\n💳 Минимальная цена за ночь: {record[7]} RUB' \
                          f'\n💳 Максимальное цена за ночь: {record[8]} RUB'
            bot.send_message(chat_id=message.chat.id, text=string)
            if error:
                bot.send_message(chat_id=message.chat.id, text='\nПри загрузке возникли ошибки, отели не загружены')
            else:
                hotels = dbworker.get_hotels(uid=uid)
                if hotels:
                    for hotel in hotels:
                        bot.send_message(chat_id=message.chat.id, text=
                        f"🏨 Название отеля: {hotel[0]}"
                        f"\n🌎 Адрес: {hotel[1]}"
                        f"\n🌐 Сайт: https://www.hotels.com/ho{hotel[2]}"
                        f"\n↔ Расстояние от центра: {hotel[4]}"
                        f"\n💳 Цена за сутки: {round(float(hotel[5]))} RUB"
                        f"\n⭐ Рейтинг посетителей: {hotel[3]}",
                                         disable_web_page_preview=True)
    else:
        bot.send_message(chat_id=message.chat.id, text='Записей не найдено')

