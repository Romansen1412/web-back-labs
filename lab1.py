from flask import Blueprint, url_for, request, redirect
import datetime
lab1 = Blueprint('lab1', __name__)

@lab1.route("/lab1")
def lab():
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


@lab1.route("/lab1/web")
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


@lab1.route("/lab1/author")
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


@lab1.route("/lab1/image")
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


@lab1.route("/lab1/counter")
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


@lab1.route("/lab1/clear")
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


@lab1.route("/lab1/info")
def info():
    return redirect("/lab1/author")


@lab1.route("/lab1/created")
def created():
    return '''<!doctype html>
        <html>
           <body>
               <h1>Созданно успешно!</h1>
               <div><i>А может, ничего и не создавалось?..</i></div>
           </body>
        </html>''', 201


@lab1.route("/lab1/400")
def bad_request():
    return "400 Bad Request — сервер не может обработать запрос из-за ошибки клиента", 400


@lab1.route("/lab1/401")
def unauthorized():
    return "401 Unauthorized — требуется аутентификация для доступа к ресурсу", 401


@lab1.route("/lab1/402")
def payment_required():
    return "402 Payment Required — зарезервировано для будущего использования", 402


@lab1.route("/lab1/403")
def forbidden():
    return "403 Forbidden — у вас нет прав доступа к этому ресурсу", 403


@lab1.route("/lab1/405")
def method_not_allowed():
    return "405 Method Not Allowed — метод запроса не поддерживается для данного ресурса", 405


@lab1.route("/lab1/418")
def teapot():
    return "418 I'm a teapot — сервер отказывается заваривать кофе, потому что он чайник", 418