import requests
import os
import json
from json import JSONDecodeError
from dotenv import load_dotenv
from loguru import logger
from requests import Response
from typing import Any

load_dotenv()

X_RAPIDAPI_KEY = os.getenv('RAPID_API_KEY')

headers = {
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
    "X-RapidAPI-Key": X_RAPIDAPI_KEY
}


def get_request(url: str, headers: {}, params: {}) -> Response:
    """Функция для выполнения запроса"""
    try:
        return requests.get(url=url, headers=headers, params=params, timeout=30)
    except requests.exceptions.RequestException as exc:
        logger.exception(exc)


def request_city(city: str) -> tuple[Any, Any]:
    """Функция для запроса к API и получения данных о городе"""
    url = "https://hotels4.p.rapidapi.com/locations/v2/search"
    querystring = {"query": city, "locale": "ru_RU", "currency": "RUB"}
    try:
        request = get_request(url=url, headers=headers, params=querystring)
        data = json.loads(request.text)
        return (data["suggestions"][0]["entities"][0]["destinationId"],
                data["suggestions"][0]["entities"][0]["name"])
    except (LookupError, TypeError) as exc:
        logger.exception(exc)


def parse_list(parse_list: list, uid: str, city: str, distance: str) -> list:
    """Функция для подготовки данных к записи в базу данных"""
    hotels = []
    hotel_id, name, adress, center, price = '', '', '', 'нет данных', ''

    for hotel in parse_list:
        try:
            hotel_id = hotel['id']
            name = hotel['name']
            adress = f'{hotel["address"]["countryName"]}, {city.capitalize()},' \
                     f' {hotel["address"].get("postalCode", "")},' \
                     f' {hotel["address"].get("streetAddress", "")}'
            if len(hotel['landmarks']) > 0:
                if hotel['landmarks'][0]['label'] == 'Центр города':
                    center = hotel['landmarks'][0]['distance']
            price = str(hotel['ratePlan']['price']['exactCurrent'])
            coordinates = f"{hotel['coordinate'].get('lat', 0)},{hotel['coordinate'].get('lon', 0)}"
            star_rating = str(hotel['starRating'])
            user_rating = hotel.get('guestReviews', {}).get('rating', 'нет данных').replace(',', '.')
            if distance != '':
                if float(distance) < float(center.split()[0].replace(',', '.')):
                    continue
            hotels.append((uid, hotel_id, name, adress, center, price, user_rating))
        except (LookupError, ValueError) as exc:
            logger.exception(exc)
            continue
    return hotels


def request_list(id: str, list_param: list) -> list:
    """Функция для запроса к API и получения основных данных"""

    url = "https://hotels4.p.rapidapi.com/properties/list"
    check_in = '-'.join(list_param[1].split('.')[::-1])
    check_out = '-'.join(list_param[2].split('.')[::-1])
    sort_order = ''
    landmark_ids = ''
    price_min = ''
    price_max = ''
    page_size = list_param[4]
    if list_param[6] == '/lowprice':
        sort_order = 'PRICE'
    elif list_param[6] == '/highprice':
        sort_order = 'PRICE_HIGHEST_FIRST'
    elif list_param[6] == '/bestdeal':
        sort_order = 'DISTANCE_FROM_LANDMARK'
        landmark_ids = 'Центр города'
        price_min = list_param[7]
        price_max = list_param[8]

    querystring = {"destinationId": id, "pageNumber": "1", "pageSize": page_size, "checkIn": check_in,
                   "checkOut": check_out, "adults1": "1", "priceMin": price_min, "priceMax": price_max,
                   "sortOrder": sort_order, "locale": "ru_RU", "currency": "RUB",
                   "landmarkIds": landmark_ids}
    try:
        request = get_request(url=url, headers=headers, params=querystring)
        data = json.loads(request.text)
        parsed = parse_list(parse_list=data['data']['body']['searchResults']['results'], uid=list_param[5],
                            city=list_param[0], distance=list_param[9])
        return parsed
    except (LookupError, JSONDecodeError, TypeError) as exc:
        logger.exception(exc)


def request_photo(id_hotel: str) -> list:
    """Функция для запроса к API и получения данных о фотографиях"""
    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
    querystring = {"id": id_hotel}
    photos = []
    try:
        response = get_request(url, headers=headers, params=querystring)
        data = json.loads(response.text)
        for photo in data['hotelImages']:
            url = photo['baseUrl'].replace('_{size}', '_z')
            photos.append((id_hotel, url))
        return photos
    except (JSONDecodeError, TypeError) as exc:
        logger.exception(exc)


def check_foto(photo: str) -> bool:
    """Функция для проверки URL фото"""
    try:
        check_photo = requests.get(url=photo, timeout=30)
        if check_photo.status_code == 200:
            return True
    except requests.exceptions.RequestException as exc:
        logger.exception(exc)

