HotelsChief Telegram-bot
Telegram-бот для поиска подходящих пользователю отелей. Работает с API от Hotels.com

Программа написана на языке Python в рамках финальной работы к курсу Python-basic от Skillbox.

Development language (Язык разработки) - Python
Language (язык): Russian
Author (Автор): Aleksandr Zaborev


Как запустить бота:
Скачать скрипт
Установить зависимости: pip install -r requirements.txt
Создать telegram-бота у BotFather и получить токен
Получить ключ от rapidapi:
Зарегистрироваться на сайте rapidapi.com
Перейти в API Marketplace → категория Travel → Hotels (либо просто перейти по прямой ссылке на документацию Hotels API Documentation)
Нажать кнопку Subscribe to Test
Выбрать пакет (есть бесплатный вариант)
Забрать KEY
Создать файл .env и прописать там BOT_TOKEN и RAPID_API_KEY так, как это представленно в файле-шаблоне .env.template
Запустить бота: python main.py


Возможности бота:
Бот реагирует на команды:

/start - Запустить бота
/help - Вывести список команд бота
/lowprice - Подбор недорогих отелей в указанном Вами городе
/highprice - Подбор отелей премиум - класса в указанном Вами городе
/bestdeal - Подбор лучших отелей в указанном городе по диапазону цен
/history - Покажу историю ваших запросов
/clear_history - Удалю историю ваших запросов


Принцип работы
После ввода команд /lowprice и /highprice бот проводит опрос пользователя:

Город для поездки
Дата заселения в отель и дата выселения
Количество отелей для вывода результата (максимум 10)
Нужно ли загрузить фото отеля
Количество фото (максимум 10)
При вводе команды /bestdeal дополнительно запрашивается:

Диапазон цен в рублях за 1 ночь
Максимальная удаленность от центра города
При удачных запросах ведется история поиска. Все запросы и их результат сохраняется в базе данных SQLLite.

При вводе команды /history пользователю выдаются все результаты поиска
При вводе команды /clear_history пользователю предлагается очистить историю поиска.
