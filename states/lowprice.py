from telebot.handler_backends import State, StatesGroup


class LowPriceState(StatesGroup):
    city = State()
    start_date = State()
    end_date = State()
    hotels_count = State()
    need_photo = State()
    photo_count = State()
    results = State()
