from flask import Flask, url_for, request, redirect, abort, render_template
import datetime
app = Flask(__name__)

@app.route("/")
@app.route("/index")
def start():
    return """<!doctype html>
    <html>
        <head>
            <title>НГТУ, ФБ, Лабораторные работы</title>
            <meta charset="utf-8">
        </head>
        <body>
            <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
            <ul>
                <li><a href="/lab1">Первая лабораторная</a></li>
            </ul>
            <hr>
            <footer>
                <p>Фисенко Роман Алексеевич</p>
                <p>Группа: ФБИ-31</p>
                <p>Курс: 3</p>
                <p>2025 год</p>
            </footer>
        </body>
    </html>"""

@app.route("/lab1")
def lab1():
    return """<!doctype html>
    <html>
        <head>
            <title>Лабораторная 1</title>
            <meta charset="utf-8">
        </head>
        <body>
            <div>
                Flask — фреймворк для создания веб-приложений на языке
                программирования Python, использующий набор инструментов
                Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
                называемых микрофреймворков — минималистичных каркасов
                веб-приложений, сознательно предоставляющих лишь самые
                базовые возможности.
            </div>
            <hr>
            <a href="/">Главное меню</a>
            <ul>
                <li><a href="/lab1/web">/lab1/web</a></li>
                <li><a href="/lab1/author">/lab1/author</a></li>
                <li><a href="/lab1/image">/lab1/image</a></li>
                <li><a href="/lab1/counter">/lab1/counter</a></li>
                <li><a href="/lab1/clear">/lab1/clear</a></li>
                <li><a href="/lab1/info">/lab1/info</a></li>
                <li><a href="/lab1/created">/lab1/created</a></li>
                <li><a href="/lab1/400">/lab1/400</a></li>
                <li><a href="/lab1/401">/lab1/401</a></li>
                <li><a href="/lab1/402">/lab1/402</a></li>
                <li><a href="/lab1/403">/lab1/403</a></li>
                <li><a href="/lab1/405">/lab1/405</a></li>
                <li><a href="/lab1/418">/lab1/418</a></li>
                <li><a href="/lab1/error">/lab1/error</a></li>
            </ul>
        </body>
    </html>"""

@app.route("/lab1/web")
def web():
    return """<!doctype html>
        <html>
           <body>
               <h1>web-сервер на flask</h1>
           </body>
        </html>""", 200, {
            'X-Server': 'sample',
            'Content-Type': 'text/plain; charset=utf-8'
        }

@app.route("/lab1/author")
def author():
    name = "Фисенко Роман Алексеевич"
    group = "ФБИ-31"
    faculty = "ФБ"

    return """<!doctype html>
    <html>
        <body>
            <p>Студент: """ + name + """</p>
            <p>Гpynna: """ + group + """</p>
            <p>Факультет: """ + faculty + """</p>
            <a href="/lab1/web">web</a>
        </body>
    </html>"""

@app.route("/lab1/image")
def image():
    path = url_for("static", filename="oak.jpg")
    path2 = url_for("static", filename="lab1.css")
    return '''<!doctype html>
        <html>
            <link rel="stylesheet" href="'''+ path2 + '''">
            <body>
                <h1>Мудрый Дуб</h1>
                <img src="''' + path + '''">
            </body>
        </html>''', {
            'Content-Type': 'text/html; charset=utf-8',
            'Content-Language': 'ru',
            'X-Author': 'Fisenko Roman A.',
            'X-Project': 'LabFlask'
        }

count = 0

@app.route("/lab1/counter")
def counter():
    global count
    count += 1
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr

    return '''<!doctype html>
        <html>
           <body>
                Сколько раз вы сюда заходили: ''' + str(count) + '''
                <hr>
                Дата и время: ''' + str(time) + '''<br>
                Запрошенный адрес: ''' + url + '''<br>
                Ваш IP-адрес: ''' + client_ip + '''<br>
                <br>
                Хотите очистить счетчик? Жмите:<br>
                <a href="/lab1/clear">clear</a>
           </body>
        </html>'''

@app.route("/lab1/clear")
def clear():
    global count
    count = 0

    return '''<!doctype html>
        <html>
           <body>
                Счетчик очищен! Не верите? Проверьте:<br>
                <a href="/lab1/counter">counter</a>
           </body>
        </html>'''

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@app.route("/lab1/created")
def created():
    return '''<!doctype html>
        <html>
           <body>
               <h1>Созданно успешно!</h1>
               <div><i>А может, ничего и не создавалось?..</i></div>
           </body>
        </html>''', 201

@app.route("/lab1/400")
def bad_request():
    return "400 Bad Request — сервер не может обработать запрос из-за ошибки клиента", 400

@app.route("/lab1/401")
def unauthorized():
    return "401 Unauthorized — требуется аутентификация для доступа к ресурсу", 401

@app.route("/lab1/402")
def payment_required():
    return "402 Payment Required — зарезервировано для будущего использования", 402

@app.route("/lab1/403")
def forbidden():
    return "403 Forbidden — у вас нет прав доступа к этому ресурсу", 403

@app.route("/lab1/405")
def method_not_allowed():
    return "405 Method Not Allowed — метод запроса не поддерживается для данного ресурса", 405

@app.route("/lab1/418")
def teapot():
    return "418 I'm a teapot — сервер отказывается заваривать кофе, потому что он чайник", 418

not_found_log = []

@app.errorhandler(404)
def not_found(err):
    client_ip = request.remote_addr
    time = str(datetime.datetime.today())
    url = request.url
    not_found_log.append(time + " пользователь " + client_ip + " зашел на адрес: " + url)
    path = url_for("static", filename="error.jpg")
    log_html = "<br>".join(not_found_log)

    return '''<!doctype html>
        <html>
            <style>
                img {
                    height: 200px;
                    width: auto;
                    border-radius: 15px;
                    box-shadow: 10px 10px 15px black;
                }
                body {
                    background-color: lightgray;
                    text-align: center;
                }
            </style>
            <body>
                <h1>Если этого нет, то может оно тебе и не надо?</h1>
                <img src="''' + path + '''">
                <p>Ваш IP: ''' + client_ip + '''</p>
                <p>Дата и время запроса: ''' + time + '''</p>
                <p>Попробуйте вернуться на <a href="/">главную страницу</a></p>
                <hr>
                <h3>Лог всех 404-запросов:</h3>
                <div style='text-align: left;'>''' + log_html + '''</div>
            </body>
        </html>''', 404


@app.route("/lab1/error")
def error():
    return 1 / 0  

@app.errorhandler(500)
def server_error(err):
    return """<!doctype html>
    <html>
        <head>
            <title>Ошибка 500</title>
            <meta charset="utf-8">
        </head>
        <body>
            <h1>500 — Внутренняя ошибка сервера</h1>
            <p>На сервере произошла непредвиденная ошибка. 
               Мы уже работаем над её исправлением!</p>
            <a href="/">Вернуться на главную</a>
        </body>
    </html>""", 500

@app.route('/lab2/a')
def a():
    return 'А слэша нету'

@app.route('/lab2/a/')
def a2():
    return 'Слэш есть'

flower_list = ['Роза', 'Тюльпан', 'Незабудка', 'Ромашка']

@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    else:
        flower = flower_list[flower_id]
        return f"""<!doctype html>
        <html>
            <body>
                <h1>Цветок №{flower_id + 1}</h1>
                <p>Название: <b>{flower}</b></p>
                <p><a href="/lab2/all_flowers">Посмотреть все цветы</a></p>
            </body>
        </html>"""


@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.append(name)
    return f"""<!doctype html>
    <html>
        <body>
            <h1>Добавлен новый цветок</h1>
            <p>Название нового цветка: {name}</p>
            <p>Всего цветов: {len(flower_list)}</p>
            <p>Полный список: {flower_list}</p>
        </body>
    </html>"""

@app.route('/lab2/add_flower/')
def add_flower_empty():
    return "Вы не задали имя цветка", 400

@app.route('/lab2/all_flowers')
def all_flowers():
    flowers_html = "<ul>"
    for f in flower_list:
        flowers_html += f"<li>{f}</li>"
    flowers_html += "</ul>"

    return f"""<!doctype html>
    <html>
        <body>
            <h1>Список всех цветов</h1>
            <p>Всего цветов: {len(flower_list)}</p>
            {flowers_html}
            <p><a href="/lab2/clear_flowers">Очистить список</a></p>
        </body>
    </html>"""

@app.route('/lab2/clear_flowers')
def clear_flowers():
    flower_list.clear()
    return """<!doctype html>
    <html>
        <body>
            <h1>Список цветов очищен!</h1>
            <p><a href="/lab2/all_flowers">Посмотреть все цветы</a></p>
        </body>
    </html>"""

@app.route('/lab2/example')
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

@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/filters')
def filters():
    phrase = 'О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных...'
    return render_template('filters.html', phrase=phrase)

@app.route('/lab2/calc/<int:a>/<int:b>')
def calcAB(a, b):
    return f"""<!doctype html>
    <html>
        <body>
            <h1>Расчет с параметрами:</h1>
            <p>{a} + {b} = {a+b}</p>
            <p>{a} - {b} = {a-b}</p>
            <p>{a} × {b} = {a*b}</p>
            <p>{a} / {b} = {a/b}</p>
            <p>{a}<sup>{b}</sup> = {a**b}</p>
        </body>
    </html>"""

@app.route('/lab2/calc/')
def calc():
    return redirect("/lab2/calc/1/1")

@app.route('/lab2/calc/<int:a>/')
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

@app.route("/lab2/books")
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

@app.route("/lab2/animals")
def lab2_animals():
    return render_template("objects.html", objects=animals)