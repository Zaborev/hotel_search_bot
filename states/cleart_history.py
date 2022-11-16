from telebot.handler_backends import State, StatesGroup


class ClearHistory(StatesGroup):
    first_state = State()
