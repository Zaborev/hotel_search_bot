from datetime import date
from telegram_bot_calendar import LSTEP, DetailedTelegramCalendar
from loader import bot


def get_calendar(user):
    calendar, step = DetailedTelegramCalendar(locale='ru', min_date=date.today()).build()
    bot.send_message(user, f"{LSTEP[step]}", reply_markup=calendar)


# @bot.callback_query_handler(func=DetailedTelegramCalendar.func())
# def cal(calendar):
#     result, key, step = DetailedTelegramCalendar(min_date=date.today()).process(calendar.data)
#     if not result and key:
#         bot.edit_message_text(f"{LSTEP[step]}",
#                               calendar.message.chat.id,
#                               calendar.message.message_id,
#                               reply_markup=key)
#     elif result:
#         bot.edit_message_text(f"Вы выбрали дату: {result}",
#                               calendar.message.chat.id,
#                               calendar.message.message_id)
#         return result
