import redis
from django.conf import settings
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MomentShare.settings')
import django

django.setup()

redis_instance = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB
)


def like_post(user_id, post_id):
    like_key = f'like:post:{post_id}'
    dislike_key = f'dislike:post:{post_id}'

    # Если уже поставлен дизлайк, удаляем его
    if redis_instance.sismember(dislike_key, user_id):
        redis_instance.srem(dislike_key, user_id)

    # Добавляем лайк, если его нет
    redis_instance.sadd(like_key, user_id)


def dislike_post(redis_instance, user_id, post_id):
    like_key = f'like:post:{post_id}'
    dislike_key = f'dislike:post:{post_id}'

    # Если уже поставлен лайк, удаляем его
    if redis_instance.sismember(like_key, user_id):
        redis_instance.srem(like_key, user_id)

    # Добавляем дизлайк, если его нет
    redis_instance.sadd(dislike_key, user_id)


def get_post_reactions(post_id):
    like_key = f'like:post:{post_id}'
    dislike_key = f'dislike:post:{post_id}'

    likes = redis_instance.scard(like_key)
    dislikes = redis_instance.scard(dislike_key)

    return {'likes': likes, 'dislikes': dislikes}


def toggle_heart(post_id, user_id):
    hearts_key = f'hearts:user:{post_id}'

    if redis_instance.sismember(hearts_key, user_id):
        redis_instance.srem(hearts_key, user_id)
        return False
    else:
        redis_instance.sadd(hearts_key, user_id)
        return True


def increment_counter(key):
    """
    Увеличивает счетчик в Redis для заданного ключа и возвращает новое значение.

    :param redis_instance: Экземпляр Redis.
    :param key: Ключ счетчика в Redis.
    :return: Новое значение счетчика.
    """
    new_count = redis_instance.incr(key)
    return {'count': new_count}


def toggle_element(key, value, return_all=False):
    """
    Добавляет или удаляет элемент из множества в Redis и возвращает информацию о состоянии множества.

    :param redis_instance: Экземпляр Redis.
    :param key: Ключ множества в Redis.
    :param value: Значение для добавления/удаления.
    :param return_all: Возвращать ли все элементы множества.
    :return: Словарь с информацией о количестве элементов, статусе (добавлен/удален) и, возможно, всеми элементами.
    """

    # Проверяем, есть ли уже элемент в множестве
    if redis_instance.sismember(key, value):
        redis_instance.srem(key, value)
        status = 'removed'
    else:
        redis_instance.sadd(key, value)
        status = 'added'

    count = redis_instance.scard(key)
    response = {'count': count, 'status': status}

    # Если требуется, добавляем список всех элементов
    if return_all:
        all_elements = redis_instance.smembers(key)
        response['elements'] = all_elements

    return response


def get_element_heart_status(key, value):
    """
    Получает статус элемента (добавлен/удален) из множества в Redis и возвращает его вместе с общим количеством элементов.

    :param redis_instance: Экземпляр Redis.
    :param key: Ключ множества в Redis.
    :param value: Значение для проверки.
    :return: Словарь с информацией о количестве элементов и статусе (добавлен/удален).
    """

    status = 'added' if redis_instance.sismember(key, value) else 'removed'
    count = redis_instance.scard(key)

    return {'count': count, 'status': status}
