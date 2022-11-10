from telebot import types
import botrequests.hotels as hotels


def create_media_group(photos: list, count) -> list:
    media_group = []
    counter = 0
    for photo in photos:
        if hotels.check_foto(photo=photo[1]):
            media_group.append(types.InputMediaPhoto(media=photo[1]))
            counter += 1
        if counter == count:
            break
    return media_group
