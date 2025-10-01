from flask import Blueprint, redirect, abort, render_template
lab2 = Blueprint('lab2', __name__)

@lab2.route('/lab2/a')
def a():
    return 'А слэша нету'

@lab2.route('/lab2/a/')
def a2():
    return 'Слэш есть'

flower_list = [
    {"name": "Роза", "price": 100},
    {"name": "Тюльпан", "price": 80},
    {"name": "Незабудка", "price": 50},
    {"name": "Ромашка", "price": 60}
]

@lab2.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    flower_name = flower_list[flower_id]
    return render_template('flower.html', flower_id=flower_id, flower_name=flower_name)

@lab2.route('/lab2/delete_flower/<int:flower_id>')
def delete_flower(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    deleted_flower = flower_list.pop(flower_id)
    return render_template('delete_flower.html', flower=deleted_flower, total=len(flower_list), flowers=flower_list)

@lab2.route('/lab2/add_flower/<name>/<int:price>')
def add_flower(name, price):
    flower_list.append({"name": name, "price": price})
    return render_template('add_flower.html', name=name, price=price, total=len(flower_list), flowers=flower_list)

@lab2.route('/lab2/add_flower/')
def add_flower_empty():
    return render_template('add_flower_empty.html'), 400

@lab2.route('/lab2/all_flowers')
def all_flowers():
    return render_template('all_flowers.html', flowers=flower_list, total=len(flower_list))

@lab2.route('/lab2/clear_flowers')
def clear_flowers():
    flower_list.clear()
    return render_template('clear_flowers.html')

@lab2.route('/lab2/example')
def example():
    name = 'Роман Фисенко'
    lab = '2'
    group = 'ФБИ-31'
    course = '2'
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 40},
        {'name': 'апельсины', 'price': 70},
        {'name': 'мандарины', 'price': 125},
        {'name': 'манго', 'price': 250}
    ]
    return render_template('example.html', name=name, lab=lab, group=group, course=course, fruits=fruits)

@lab2.route('/lab2/')
def lab22():
    return render_template('lab2.html')

@lab2.route('/lab2/filters')
def filters():
    phrase = 'О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных...'
    return render_template('filters.html', phrase=phrase)

@lab2.route('/lab2/calc/<int:a>/<int:b>')
def calcAB(a, b):
    return render_template("calc.html", a=a, b=b)

@lab2.route('/lab2/calc/')
def calc():
    return redirect("/lab2/calc/1/1")

@lab2.route('/lab2/calc/<int:a>/')
def calcA(a):
    return redirect(f"/lab2/calc/{a}/1")

books = [
    {"author": "Лев Толстой", "title": "Война и мир", "genre": "Роман", "pages": 1225},
    {"author": "Фёдор Достоевский", "title": "Преступление и наказание", "genre": "Роман", "pages": 671},
    {"author": "Александр Пушкин", "title": "Евгений Онегин", "genre": "Роман в стихах", "pages": 400},
    {"author": "Михаил Булгаков", "title": "Мастер и Маргарита", "genre": "Мистика", "pages": 480},
    {"author": "Иван Тургенев", "title": "Отцы и дети", "genre": "Роман", "pages": 320},
    {"author": "Николай Гоголь", "title": "Мёртвые души", "genre": "Поэма", "pages": 352},
    {"author": "Антон Чехов", "title": "Вишнёвый сад", "genre": "Пьеса", "pages": 120},
    {"author": "Владимир Набоков", "title": "Лолита", "genre": "Роман", "pages": 432},
    {"author": "Даниил Гранин", "title": "Иду на грозу", "genre": "Роман", "pages": 500},
    {"author": "Борис Пастернак", "title": "Доктор Живаго", "genre": "Роман", "pages": 592}
]

@lab2.route("/lab2/books")
def lab2_books():
    return render_template("books.html", books=books)

animals = [
    {"name": "Котик", "desc": "Милый пушистый кот", "img": "Cat.jpg"},
    {"name": "Собака", "desc": "Весёлый щенок", "img": "Dog.jpg"},
    {"name": "Черепаха", "desc": "Медлительное существо с панцирем", "img": "Turtle.jpg"},
    {"name": "Хомяк", "desc": "Маленький грызун", "img": "Hamster.jpg"},
    {"name": "Крокодил", "desc": "Опасный хищник", "img": "Crocodile.jpg"},
    {"name": "Паук", "desc": "Охотник на насекомых и грызунов", "img": "Spider.jpg"},
    {"name": "Жираф", "desc": "Высокое животное с длинной шеей", "img": "Giraffe.jpg"},
    {"name": "Голубь", "desc": "Миролюбивая птица", "img": "Pigeon.jpg"},
    {"name": "Жук-носорог", "desc": "Маленький жук с рогом", "img": "Rhinoceros beetle.jpg"},
    {"name": "Плащеносная акула", "desc": "Редкая глубоководная акула", "img": "Frilled shark.jpg"},
    {"name": "Гусь", "desc": "Птица с длинной шеей", "img": "Goose.jpg"},
    {"name": "Носорог", "desc": "Большое животное с рогом", "img": "Rhino.jpg"},
    {"name": "Крылатка-зебра", "desc": "Ядовитая и красочная морская рыба", "img": "Red lionfish.jpg"},
    {"name": "Лев", "desc": "Царь зверей", "img": "Lion.jpg"},
    {"name": "Обезьяна", "desc": "Как жизнь, брат?", "img": "Monkey.jpg"},
    {"name": "Медведь", "desc": "Большое лесное животное", "img": "Bear.jpg"},
    {"name": "Пингвин", "desc": "Не умеет летать, но отлично плавает", "img": "Penguin.jpg"},
    {"name": "Наутилус", "desc": "Морской моллюск с раковиной", "img": "Nautilus.jpg"},
    {"name": "Лось", "desc": "Крупный лесной зверь", "img": "Moose.jpg"}
]

@lab2.route("/lab2/animals")
def lab2_animals():
    return render_template("objects.html", objects=animals)