from flask import Blueprint, render_template, request, abort, jsonify
from datetime import datetime
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import current_app
from os import path

lab7 = Blueprint('lab7', __name__)

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='roman_fis_knowledge_base',
            user='roman_fis_knowledge_base',
            password='123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    return conn, cur


def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

def validate_film(film):
    errors = {}

    if not film.get('title_ru', '').strip():
        errors['title_ru'] = 'Введите название на русском'

    if not film.get('title', '').strip() and film.get('title_ru', '').strip() == '':
        errors['title'] = 'Введите оригинальное название'

    year = film.get('year')
    current_year = datetime.now().year
    try:
        year = int(year)
        if year < 1895 or year > current_year:
            errors['year'] = f'Год должен быть между 1895 и {current_year}'
    except:
        errors['year'] = 'Год должен быть числом'

    desc = film.get('description', '').strip()
    if not desc:
        errors['description'] = 'Заполните описание'
    elif len(desc) > 2000:
        errors['description'] = 'Описание не должно превышать 2000 символов'

    return errors if errors else None


@lab7.route('/lab7/')
def lab():
    return render_template('lab7/index.html')

# films = [
#   {
#     "title": "The Shawshank Redemption",
#     "title_ru": "Побег из Шоушенка",
#     "year": 1994,
#     "description": "Два заключенных сближаются за долгие годы, находя\
#         утешение и в конечном итоге искупление через акты человеческого достоинства."
#   },
#   {
#     "title": "The Godfather",
#     "title_ru": "Крестный отец",
#     "year": 1972,
#     "description": "Стареющий глава династии организованной преступности передает\
#         контроль над своей тайной империей своему нерешительному сыну."
#   },
#   {
#     "title": "The Dark Knight",
#     "title_ru": "Темный рыцарь",
#     "year": 2008,
#     "description": "Когда угроза, известная как Джокер, сеет хаос и разрушения в Готэме, Бэтмену приходится\
#         столкнуться с величайшим психологическим и физическим испытанием его способности бороться с несправедливостью."
#   },
#   {
#     "title": "Pulp Fiction",
#     "title_ru": "Криминальное чтиво",
#     "year": 1994,
#     "description": "Жизни двух наемных убийц, боксера, гангстера и его жены, а также пары грабителей в закусочной\
#         переплетаются в четырех историях о насилии и искуплении."
#   },
#   {
#     "title": "The Lord of the Rings: The Return of the King",
#     "title_ru": "Властелин колец: Возвращение короля",
#     "year": 2003,
#     "description": "Гэндальф и Арагорн ведут Мир Людей против армии Саурона, чтобы дать Фродо и Сэму шанс уничтожить Единое Кольцо."
#   }
# ]

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id, title, title_ru, year, description FROM films ORDER BY id;")
    else:
        cur.execute("SELECT id, title, title_ru, year, description FROM films ORDER BY id;")
    films = cur.fetchall()
    db_close(conn, cur)
    return jsonify(films)


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id, title, title_ru, year, description FROM films WHERE id = %s;", (id,))
    else:
        cur.execute("SELECT id, title, title_ru, year, description FROM films WHERE id = ?;", (id,))
    film = cur.fetchone()
    db_close(conn, cur)
    if not film:
        abort(404)
    return jsonify(film)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("DELETE FROM films WHERE id=%s;", (id,))
    else:
        cur.execute("DELETE FROM films WHERE id=?;", (id,))
    db_close(conn, cur)
    return '', 204
        
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    film = request.get_json()

    if not film.get('title') and film.get('title_ru'):
        film['title'] = film['title_ru']

    errors = validate_film(film)
    if errors:
        return errors, 400

    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(
            "UPDATE films SET title=%s, title_ru=%s, year=%s, description=%s WHERE id=%s;",
            (film['title'], film['title_ru'], film['year'], film['description'], id)
        )
    else:
        cur.execute(
            "UPDATE films SET title=?, title_ru=?, year=?, description=? WHERE id=?;",
            (film['title'], film['title_ru'], film['year'], film['description'], id)
        )
    db_close(conn, cur)
    film['id'] = id
    return jsonify(film)

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()
    if not film.get('title') and film.get('title_ru'):
        film['title'] = film['title_ru']

    errors = validate_film(film)
    if errors:
        return errors, 400

    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(
            "INSERT INTO films (title, title_ru, year, description) VALUES (%s, %s, %s, %s) RETURNING id;",
            (film['title'], film['title_ru'], film['year'], film['description'])
        )
        film_id = cur.fetchone()['id']
    else:
        cur.execute(
            "INSERT INTO films (title, title_ru, year, description) VALUES (?, ?, ?, ?);",
            (film['title'], film['title_ru'], film['year'], film['description'])
        )
        film_id = cur.lastrowid
    db_close(conn, cur)
    film['id'] = film_id
    return jsonify(film)
