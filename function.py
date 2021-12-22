import json
import sqlite3

def get_list(sqlite_query):
    """

    :param sqlite_query:
    :return:
    """
    with sqlite3.connect("netflix.db") as connection:  # Подключаемся к БД
        cursor = connection.cursor()  # Запускаем курсор, с помощью которого мы будем получать данные из БД

        cursor.execute(sqlite_query)  # Выполняем запрос с помощью курсора
        list_db = cursor.fetchall()  # С помощью этой функции получаем результат запроса в виде списка кортежей

    return list_db

def get_list_new(sqlite_query):
    """

    :param sqlite_query:
    :return:
    """
    with sqlite3.connect("netflix.db") as connection:  # Подключаемся к БД
        connection.row_factory = sqlite3.Row #именует
        cursor = connection.cursor()  # Запускаем курсор, с помощью которого мы будем получать данные из БД
        cursor.execute(sqlite_query)  # Выполняем запрос с помощью курсора
        list_db = cursor.fetchall()  # С помощью этой функции получаем результат запроса в виде списка кортежей

    return list_db



query = f"""
        SELECT title, rating, description
        FROM netflix
        WHERE rating LIKE '%G%'
        LIMIT 10
    """

a = (get_list_new(query))

for i in a:
    print(dict(i))