from flask import Flask, url_for, request
import datetime
import os
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'top secret key')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)

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
                <li><a href="/lab2/">Вторая лабораторная</a></li>
                <li><a href="/lab3/">Третья лабораторная</a></li>
                <li><a href="/lab4/">Четвертая лабораторная</a></li>
                <li><a href="/lab5/">Пятая лабораторная</a></li>
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

not_found_log = []

@app.errorhandler(404)
def not_found(err):
    client_ip = request.remote_addr
    time = str(datetime.datetime.today())
    url = request.url
    not_found_log.append(time + " пользователь " + client_ip + " зашел на адрес: " + url)
    path = url_for("static", filename="lab1/error.jpg")
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
