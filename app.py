from flask import Flask, url_for, request
import datetime
import os
from os import path
from db import db
from flask_sqlalchemy import SQLAlchemy
from db.models import users
from flask_login import LoginManager

from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8
from lab9 import lab9
from RGZ import rgz

app = Flask(__name__)

login_manager = LoginManager()
login_manager.login_view = 'lab8.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(login_id):
    return users.query.get(int(login_id))

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'top secret key')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')

if app.config['DB_TYPE'] == 'postgres':
    db_name = 'roman_fis_orm'
    db_user = 'roman_fis_orm'
    db_password = '123'
    host_ip = '127.0.0.1'
    host_port = '5432'

    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{host_ip}:{host_port}/{db_name}'
else:
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, 'roman_fis_orm.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

db.init_app(app)

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)
app.register_blueprint(lab9)
app.register_blueprint(rgz)

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
                <li><a href="/lab6/">Шестая лабораторная</a></li>
                <li><a href="/lab7/">Седьмая лабораторная</a></li>
                <li><a href="/lab8/">Восьмая лабораторная</a></li>
                <li><a href="/lab9/">Девятая лабораторная</a></li>
                <li><a href="/rgz/">Расчетно-графическая работа</a></li>
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
