import os
from dotenv import load_dotenv, find_dotenv
from datetime import datetime

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

db_file = "base.db"
BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')
DEFAULT_COMMANDS = (
    ('start', "Запустить бота"),
    ('help', "Вывести список команд бота"),
    ('hello_world', "Тестовое приветствие"),
    ('lowprice', "Подбор недорогих отелей в указанном Вами городе"),
    ('highprice', "Подбор отелей премиум - класса в указанном Вами городе"),
    ('bestdeal', "Подбор лучших отелей в указанном городе по диапазону цен"),
    ('history', "Покажу историю ваших запросов"),
)

""" Настройки по умолчанию: """
price_min = '0'
price_max = '100000'
people_count = '1'
distance = '20.0'
current_day = datetime.now().date()
date_and_time = datetime.now()
