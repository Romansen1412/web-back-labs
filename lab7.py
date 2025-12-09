from flask import Blueprint, render_template, request, redirect, session, abort

lab7 = Blueprint('lab7', __name__)

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
