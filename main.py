# Структура таблицы
# -----------------------
# show_id — id тайтла
# type — фильм или сериал
# title — название
# director — режиссер
# cast — основные актеры
# country — страна производства
# date_added — когда добавлен на Нетфликс
# release_year — когда выпущен в прокат
# rating — возрастной рейтинг
# duration — длительность
# duration_type — минуты или сезоны
# listed_in — список жанров и подборок
# description — краткое описание
from flask import Flask, request, jsonify
from function import get_list, get_list_new
app = Flask(__name__)


@app.route("/movie/title/<title>")
def page_search(title):
    query = f"""
        SELECT title, country, release_year, listed_in, description
        FROM netflix
        WHERE title LIKE '%{title}%'
        ORDER BY release_year DESC
        LIMIT 1
    """
    films = get_list(query)
    dict_films = {
        "title": films[0][0],
        "country": films[0][1],
        "release_year": films[0][2],
        "genre": films[0][3],
        "description": films[0][4]
        }

    return jsonify(dict_films)


@app.route("/movie/year")
def page_search_years():
    from_ = request.args.get("from")
    to = request.args.get("to")
    query = f"""
            SELECT title, release_year
            FROM netflix
            WHERE release_year BETWEEN {from_} AND {to}
            LIMIT 100
        """
    film_list = get_list_new(query)
    film_list_conv = [dict(i) for i in film_list]

    return jsonify(film_list_conv)


@app.route("/rating/children")
def page_rating_children():
    query = """
                SELECT title, rating, description
                FROM netflix
                WHERE rating = 'G'
            """
    film_list = get_list_new(query)
    film_list_conv = [dict(i) for i in film_list]

    return jsonify(film_list_conv)

@app.route("/rating/family")
def page_rating_family():
    query = """
                SELECT title, rating, description
                FROM netflix
                WHERE rating = 'PG' OR rating =  'PG-13'
            """
    film_list = get_list_new(query)
    film_list_conv = [dict(i) for i in film_list]

    return jsonify(film_list_conv)

@app.route("/rating/adult")
def page_rating_adult():
    query = """
                SELECT title, rating, description
                FROM netflix
                WHERE rating = 'R' OR rating = 'NC-17'
            """
    film_list = get_list_new(query)
    film_list_conv = [dict(i) for i in film_list]

    return jsonify(film_list_conv)


if __name__ == "__main__":
    app.run(debug=True)