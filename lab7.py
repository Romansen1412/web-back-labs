from flask import Blueprint, render_template, request, redirect, session, abort
from datetime import datetime

lab7 = Blueprint('lab7', __name__)

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

films = [
  {
    "title": "The Shawshank Redemption",
    "title_ru": "Побег из Шоушенка",
    "year": 1994,
    "description": "Два заключенных сближаются за долгие годы, находя\
        утешение и в конечном итоге искупление через акты человеческого достоинства."
  },
  {
    "title": "The Godfather",
    "title_ru": "Крестный отец",
    "year": 1972,
    "description": "Стареющий глава династии организованной преступности передает\
        контроль над своей тайной империей своему нерешительному сыну."
  },
  {
    "title": "The Dark Knight",
    "title_ru": "Темный рыцарь",
    "year": 2008,
    "description": "Когда угроза, известная как Джокер, сеет хаос и разрушения в Готэме, Бэтмену приходится\
        столкнуться с величайшим психологическим и физическим испытанием его способности бороться с несправедливостью."
  },
  {
    "title": "Pulp Fiction",
    "title_ru": "Криминальное чтиво",
    "year": 1994,
    "description": "Жизни двух наемных убийц, боксера, гангстера и его жены, а также пары грабителей в закусочной\
        переплетаются в четырех историях о насилии и искуплении."
  },
  {
    "title": "The Lord of the Rings: The Return of the King",
    "title_ru": "Властелин колец: Возвращение короля",
    "year": 2003,
    "description": "Гэндальф и Арагорн ведут Мир Людей против армии Саурона, чтобы дать Фродо и Сэму шанс уничтожить Единое Кольцо."
  }
]

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return films


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if 0 <= id < len(films):
        return films[id]
    else:
        abort(404)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    if 0 <= id < len(films):
        del films[id]
        return '', 204
    else:
        abort(404)
        
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if 0 <= id < len(films):
        film = request.get_json()
        if not film.get('title') and film.get('title_ru'):
            film['title'] = film['title_ru']

        errors = validate_film(film)
        if errors:
            return errors, 400

        films[id] = film
        return films[id]
    else:
        abort(404)

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()
    if not film.get('title') and film.get('title_ru'):
        film['title'] = film['title_ru']

    errors = validate_film(film)
    if errors:
        return errors, 400

    films.append(film)
    new_id = len(films) - 1
    return films[new_id]