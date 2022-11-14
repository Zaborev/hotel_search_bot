from telebot.handler_backends import State, StatesGroup


class BestDealState(StatesGroup):
    city = State()
    price_min = State()
    price_max = State()
    distance = State()
    hotels_count = State()
    need_photo = State()
    photo_count = State()
    results = State()
