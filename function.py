import json
import sqlite3
from collections import Counter

def get_list(sqlite_query):
    """
    функция подключается к бд и выводит запрос в виде списка кортежей
    :param sqlite_query: str sql запрос
    :return: list
    """
    with sqlite3.connect("netflix.db") as connection:  # Подключаемся к БД
        cursor = connection.cursor()  # Запускаем курсор, с помощью которого мы будем получать данные из БД
        cursor.execute(sqlite_query)  # Выполняем запрос с помощью курсора
        list_db = cursor.fetchall()  # С помощью этой функции получаем результат запроса в виде списка кортежей

    return list_db

def get_list_new(sqlite_query):
    """
    функция подключается к бд и выводит запрос в виде списка кортежей только с использованием sqlite3.Row row_factory
    :param sqlite_query:
    :return:
    """
    with sqlite3.connect("netflix.db") as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute(sqlite_query)
        list_db = cursor.fetchall()

    return list_db


def search_listed_in(listed_in):
    """
    которая получает название жанра в качестве аргумента
    и возвращает 10 самых свежих фильмов в формате json
    :param listed_in: str
    :return: json
    """
    query = f"""
            SELECT title, description
            FROM netflix
            WHERE listed_in LIKE '%{listed_in}%'
            ORDER BY release_year DESC
            LIMIT 10
        """

    list_db = get_list_new(query)
    return json.dumps([dict(result) for result in list_db], ensure_ascii=False, indent=4)

def search_cast(actor1, actor2):
    """
    функция выводит список актеров которые играли в фильме более двух раз с задаными атерами
    :param actor1: str
    :param actor2: str
    :return: list
    """
    query = f"""
            SELECT `cast`
            FROM netflix
            WHERE `cast` LIKE '%{actor1}%' AND `cast` LIKE '%{actor2}%'
        """
    list_db = get_list(query)
    actor_list = []
    finish_actor_list = []
    for i in list_db:
        for actor in i[0].split(", "):
            if actor != actor1 and actor != actor2:
                actor_list.append(actor)

    dict_actors = Counter(actor_list)

    for actor, count in dict_actors.items():
        if count >= 2:
            finish_actor_list.append(actor)

    return finish_actor_list

def get_sort_films(type, release_year, listed_in):
    """
    функиця выводит в формете json список фильмов с описанием по заданым параметрам: тип, дата выпуска, жанр
    :param type: str
    :param release_year: int
    :param listed_in: str
    :return: json
    """
    query = f"""
                SELECT title, description
                FROM netflix
                WHERE type = "{type}" AND release_year = {release_year} AND listed_in LIKE "{listed_in}"
            """
    db = get_list_new(query)

    return json.dumps([dict(result) for result in db], ensure_ascii=False, indent=4)


#проверки

#print(search_listed_in("Comedies"))
#print(search_cast("Rose McIver", "Ben Lamb"))
#print(get_sort_films('Movie', 2010, 'Comedies'))
