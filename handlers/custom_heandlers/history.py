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
            string = f'Дата и время запроса: {record[1]}' \
                     f'\nКоманда: {record[2]}' \
                     f'\nГород: {record[3]}' \
                     f'\nКоличество отелей для поиска: {record[4]}' \
                     f'\nМаксимальное расстояние от центра: {record[9]} км'
            if record[2] == '/bestdeal':
                string += f'\nДата заезда: {record[5]}' \
                          f'\nДата выезда: {record[6]}' \
                          f'\nМинимальная цена за ночь: {record[7]} RUB' \
                          f'\nМаксимальное цена за ночь: {record[8]} RUB'
            bot.send_message(chat_id=message.chat.id, text=string)
            if error:
                bot.send_message(chat_id=message.chat.id, text='\nПри загрузке возникли ошибки, отели не загружены')
            else:
                hotels = dbworker.get_hotels(uid=uid)
                if hotels:
                    for hotel in hotels:
                        bot.send_message(chat_id=message.chat.id, text=
                        f"Название отеля: {hotel[0]}"
                        f"\nАдрес: {hotel[1]}"
                        f"\nСайт: https://www.hotels.com/ho{hotel[2]}"
                        f"\nРасстояние от центра: {hotel[4]}"
                        f"\nЦена за сутки: {round(float(hotel[5]))} RUB"
                        f"\nРейтинг по мнению посетителей: {hotel[3]}",
                                         disable_web_page_preview=True)
    else:
        bot.send_message(chat_id=message.chat.id, text='Записей не найдено')

