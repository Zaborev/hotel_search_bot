from keyboards.reply.contact import request_contact
from loader import bot
from states.contact_information import UserInfoState
from telebot.types import Message


@bot.message_handler(commands=['survey'])
def survey(message: Message) -> None:
    bot.set_state(message.from_user.id, UserInfoState.name, message.chat.id)
    bot.send_message(message.from_user.id, f'{message.from_user.username}, введите своё имя')


@bot.message_handler(state=UserInfoState.name)
def get_name(message: Message) -> None:
    if message.text.isalpha():
        bot.send_message(message.from_user.id, 'Спасибо, запомнил. Введите свой возраст.')
        bot.set_state(message.from_user.id, UserInfoState.age, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['name'] = message.text
    else:
        bot.send_message(message.from_user.id, f'Повторите ввод, имя должно содержать только буквы!')


@bot.message_handler(state=UserInfoState.age)
def get_age(message: Message) -> None:
    if message.text.isdigit():
        bot.send_message(message.from_user.id, 'Спасибо, запомнил. Теперь введите страну проживания.')
        bot.set_state(message.from_user.id, UserInfoState.country, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['age'] = message.text
    else:
        bot.send_message(message.from_user.id, f'Повторите ввод, возраст должен содержать только цифры!')


@bot.message_handler(state=UserInfoState.country)
def get_country(message: Message) -> None:
    bot.send_message(message.from_user.id, 'Спасибо, запомнил. Введите свой город.')
    bot.set_state(message.from_user.id, UserInfoState.city, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['country'] = message.text


@bot.message_handler(state=UserInfoState.city)
def get_city(message: Message) -> None:
    bot.send_message(message.from_user.id, 'Спасибо, запомнил. Отправь свой номер, нажав на кнопку',
                     reply_markup=request_contact())
    bot.set_state(message.from_user.id, UserInfoState.phone_number, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['city'] = message.text


@bot.message_handler(content_types=['text', 'contact'], state=UserInfoState.phone_number)
def get_contact(message: Message) -> None:
    if message.content_type == 'contact':
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['phone_number'] = message.contact.phone_number
            text = f'Спасибо, вся информация сохранена.\n' \
                   f'Имя: {data["name"]}\n' \
                   f'Возраст: {data["age"]}\n' \
                   f'Страна: {data["country"]}\n' \
                   f'Город: {data["city"]}\n' \
                   f'Номер телефона: {data["phone_number"]}'
            bot.send_message(message.from_user.id, text)
    else:
        bot.send_message(message.from_user.id, 'Чтобы отправить информацию, нажмите на кнопку')
