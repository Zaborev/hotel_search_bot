import sqlite3 as sq
from typing import Union
from loguru import logger
from config_data import config


def create_tables() -> None:
    """Функция для создания БД и создания таблиц"""
    with sq.connect(config.db_file) as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS history(
               id INTEGER PRIMARY KEY autoincrement,
               uid TEXT,
               chat_id TEXT,
               datetime TEXT,
               city TEXT,
               checkin TEXT,
               checkout TEXT,
               quantity TEXT, 
               quantity_photos TEXT,
               Error BOOLEAN,
               commands TEXT,
               price_min TEXT,
               price_max TEXT,
               distance TEXT);
            """)
        cur.execute("""CREATE TABLE IF NOT EXISTS hotels(
               id INTEGER PRIMARY KEY autoincrement,
               uid TEXT,
               hotel_id TEXT,
               name TEXT,
               adress TEXT,
               center TEXT,
               price TEXT,
               user_rating TEXT);
            """)
        cur.execute("""CREATE TABLE IF NOT EXISTS photos(
                 id INTEGER PRIMARY KEY autoincrement,
                 hotel_id TEXT,
                 photo TEXT);
              """)


def get_data(string: str) -> list:
    """Функция для получения данных из базы данных"""
    with sq.connect(config.db_file) as con:
        cur = con.cursor()
        try:
            cur.execute(string)
        except Exception:
            pass
        return cur.fetchall()


def delete_tables(*args) -> None:
    """Функция для удаления таблиц из базы данных"""
    with sq.connect(config.db_file) as con:
        cur = con.cursor()
        for table in args:
            cur.execute(f"DROP TABLE IF EXISTS {table}")


def get_all_from_table(table: str) -> list:
    """Функция для получения всех данных из одной таблицы"""
    with sq.connect(config.db_file) as con:
        cur = con.cursor()
        cur.execute(f"SELECT * from {table}")
        return cur.fetchall()


def set_data(string, values=tuple(), multiple=False) -> bool:
    """Функция для записи данных в базу данных"""
    with sq.connect(config.db_file) as con:
        cur = con.cursor()
        try:
            if multiple:
                cur.executemany(string, values)
            elif len(values) != 0:
                cur.execute(string, values)
            else:
                cur.execute(string)
            return True
        except sq.Error as exc:
            logger.exception(exc)


def check_data(string: str) -> Union[str, int]:
    """Функция для проверки существования записи в таблице"""
    with sq.connect(config.db_file) as con:
        cur = con.cursor()
        try:
            cur.execute(string)
            return cur.fetchone()[0]
        except (sq.Error, Exception) as exc:
            logger.exception(exc)


def set_history(history: tuple) -> bool:
    """Функция для записи данных в таблицу history"""
    return set_data(string=
                    f"INSERT INTO history(uid, chat_id, datetime, city, checkin, checkout, quantity, quantity_photos, Error, commands, price_min, price_max, distance) "
                    f"VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                    values=history)


def get_history(id: str) -> list:
    """Функция для получения данных из таблицы history"""
    history = get_data(
        string=f"SELECT uid, datetime, commands, city, quantity, checkin, checkout, price_min, price_max, distance, Error from history WHERE chat_id = '{id}'")
    return history


def get_hotels(uid: str) -> list:
    """Функция для получения данных из таблицы hotels"""
    hotels = get_data(
        string=f"SELECT name, adress, hotel_id, user_rating, center, price from hotels WHERE uid = '{uid}'")
    return hotels


def set_hotels(hotels: tuple) -> bool:
    """Функция для записи данных в таблицу hotels"""
    return set_data(string=
                    f"INSERT INTO hotels(uid, hotel_id, name, adress, center, price, user_rating) VALUES(?, ?, ?, ?, ?, ?, ?);",
                    values=hotels, multiple=True)


def get_photos(hotel_id: str, limit: str) -> list:
    """Функция для получения данных из таблицы photos"""
    return get_data(f"SELECT photo from photos WHERE hotel_id = '{hotel_id}' LIMIT '{limit}'")


def set_photos(photos: tuple) -> bool:
    """Функция для записи данных в таблицу photos"""
    return set_data(string=f"INSERT INTO photos(hotel_id, photo) VALUES(?, ?);", values=photos, multiple=True)


def check_photo(hotel_id: str) -> int:
    """Функция для проверки существования данных в таблице photos"""
    return check_data(string=f"SELECT Count(photo) FROM photos WHERE hotel_id = {hotel_id};")
