from telebot.handler_backends import State, StatesGroup


class LowPriceState(StatesGroup):
    city = State()
    hotels_count = State()
    need_photo = State()
    photo_count = State()
