from flask import Flask, url_for, request, redirect
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
                веб-приложений, сознательно предоставляющих лишь самые ба
                зовые возможности.
            </div>
            <hr>
            <li><a href="/">Главное меню</a></li>
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
        </html>'''

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

@app.errorhandler(404)
def not_found(err):
    return "Такой страницы не существует", 404