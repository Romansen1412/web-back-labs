from flask import Blueprint, render_template, request, session, redirect, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

lab5 = Blueprint("lab5", __name__)


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


@lab5.route('/lab5/')
def main():
    login = session.get('login', 'Anonymous')
    return render_template('lab5/lab5.html', login=login)


@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    session.pop('login', None)
    if request.method == 'GET':
        return render_template('lab5/register.html')
    
    login = request.form.get("login")
    password = request.form.get("password")
    full_name = request.form.get("full_name")
    
    if not login or not password:
        return render_template("lab5/register.html", error="Заполните все поля")
    
    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT login FROM users WHERE login=?;", (login,))
    
    if cur.fetchone():
        db_close(conn, cur)
        return render_template("lab5/register.html", error="Такой пользователь уже существует")
    
    password_hash = generate_password_hash(password)

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO users (login, password, full_name) VALUES (%s, %s, %s);", (login, password_hash, full_name))
    else:
        cur.execute("INSERT INTO users (login, password, full_name) VALUES (?, ?, ?);", (login, password_hash, full_name))
    
    db_close(conn, cur)
    return render_template("lab5/success.html", login=login)


@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')
    
    login = request.form.get("login")
    password = request.form.get("password")
    
    if not login or not password:
        return render_template("lab5/login.html", error="Заполните все поля")
    
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))

    user = cur.fetchone()
    
    if not user or not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template("lab5/login.html", error="Логин и/или пароль неверны")
    
    session['login'] = login
    db_close(conn, cur)
    return render_template("lab5/success_login.html", login=login)


@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    if request.method == 'GET':
        return render_template('lab5/create_article.html')

    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_public = bool(request.form.get('is_public'))

    if not title or not article_text.strip():
        return render_template('lab5/create_article.html', error="Заполните все поля", title=title, article_text=article_text, is_public=is_public)

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    
    login_id = cur.fetchone()["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(
            "INSERT INTO articles(user_id, title, article_text, is_public, is_favorite) VALUES (%s, %s, %s, %s, FALSE);",
            (login_id, title, article_text, is_public)
        )
    else:
        cur.execute(
            "INSERT INTO articles(user_id, title, article_text, is_public, is_favorite) VALUES (?, ?, ?, ?, 0);",
            (login_id, title, article_text, is_public)
        )

    db_close(conn, cur)
    return redirect('/lab5/list')



@lab5.route('/lab5/list')
def list():
    login = session.get('login')  # None если не залогинен
    
    conn, cur = db_connect()
    
    user_id = None
    if login:
        # Получаем id текущего пользователя
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
        else:
            cur.execute("SELECT id FROM users WHERE login=?;", (login,))
        result = cur.fetchone()
        if result:
            user_id = result["id"]
    
    # Выбираем статьи
    if current_app.config['DB_TYPE'] == 'postgres':
        if user_id:  # залогинен — свои + публичные
            cur.execute("SELECT * FROM articles WHERE is_public=TRUE OR user_id=%s ORDER BY is_favorite DESC;", (user_id,))
        else:  # не залогинен — только публичные
            cur.execute("SELECT * FROM articles WHERE is_public=TRUE ORDER BY is_favorite DESC;")
    else:  # sqlite
        if user_id:
            cur.execute("SELECT * FROM articles WHERE is_public=1 OR user_id=? ORDER BY is_favorite DESC;", (user_id,))
        else:
            cur.execute("SELECT * FROM articles WHERE is_public=1 ORDER BY is_favorite DESC;")
    
    articles = cur.fetchall()
    db_close(conn, cur)
    return render_template('lab5/articles.html', articles=articles, login=login, user_id=user_id)


@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)
    return redirect('/lab5')

@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    # Получаем id текущего пользователя
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    user_id = cur.fetchone()["id"]

    # Проверяем, принадлежит ли статья пользователю
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE id=%s AND user_id=%s;", (article_id, user_id))
    else:
        cur.execute("SELECT * FROM articles WHERE id=? AND user_id=?;", (article_id, user_id))
    article = cur.fetchone()

    if not article:
        db_close(conn, cur)
        return "У вас нет прав на редактирование этой статьи", 403

    if request.method == 'GET':
        db_close(conn, cur)
        return render_template('lab5/edit_article.html', article=article)

    # Обновление статьи
    title = request.form.get('title')
    article_text = request.form.get('article_text')

    if not title or not article_text.strip():
        db_close(conn, cur)
        return render_template('lab5/edit_article.html', article=article, error="Поля не могут быть пустыми")

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("UPDATE articles SET title=%s, article_text=%s WHERE id=%s;", (title, article_text, article_id))
    else:
        cur.execute("UPDATE articles SET title=?, article_text=? WHERE id=?;", (title, article_text, article_id))

    db_close(conn, cur)
    return redirect('/lab5/list')


@lab5.route('/lab5/delete/<int:article_id>', methods=['POST'])
def delete_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    # Получаем id текущего пользователя
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    user_id = cur.fetchone()["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE id=%s AND user_id=%s;", (article_id, user_id))
    else:
        cur.execute("SELECT * FROM articles WHERE id=? AND user_id=?;", (article_id, user_id))
    article = cur.fetchone()

    if not article:
        db_close(conn, cur)
        return "У вас нет прав на удаление этой статьи", 403

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("DELETE FROM articles WHERE id=%s;", (article_id,))
    else:
        cur.execute("DELETE FROM articles WHERE id=?;", (article_id,))

    db_close(conn, cur)
    return redirect('/lab5/list')

@lab5.route('/lab5/users')
def users_list():
    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login, full_name FROM users;")
    else:
        cur.execute("SELECT login, full_name FROM users;")
    users = cur.fetchall()
    db_close(conn, cur)
    return render_template('lab5/users.html', users=users)

@lab5.route('/lab5/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()
    # Получаем текущее имя пользователя
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT full_name FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT full_name FROM users WHERE login=?;", (login,))
    user = cur.fetchone()
    
    if request.method == 'GET':
        db_close(conn, cur)
        return render_template('lab5/edit_profile.html', full_name=user['full_name'], error=None)

    full_name = request.form.get('full_name', '').strip()
    password = request.form.get('password', '')
    confirm_password = request.form.get('confirm_password', '')

    if not full_name:
        db_close(conn, cur)
        return render_template('lab5/edit_profile.html', full_name=full_name, error="Имя не может быть пустым")
    
    if password and password != confirm_password:
        db_close(conn, cur)
        return render_template('lab5/edit_profile.html', full_name=full_name, error="Пароли не совпадают")

    # Обновляем имя и/или пароль
    if password:
        password_hash = generate_password_hash(password)
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute(
                "UPDATE users SET full_name=%s, password=%s WHERE login=%s;",
                (full_name, password_hash, login)
            )
        else:
            cur.execute(
                "UPDATE users SET full_name=?, password=? WHERE login=?;",
                (full_name, password_hash, login)
            )
    else:
        # Если пароль не указан, меняем только имя
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE users SET full_name=%s WHERE login=%s;", (full_name, login))
        else:
            cur.execute("UPDATE users SET full_name=? WHERE login=?;", (full_name, login))

    db_close(conn, cur)
    return redirect('/lab5')

@lab5.route('/lab5/toggle_favorite/<int:article_id>', methods=['POST'])
def toggle_favorite(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()
    if current_app.config['DB_TYPE']=='postgres':
        cur.execute("SELECT is_favorite FROM articles WHERE id=%s;", (article_id,))
        current = cur.fetchone()['is_favorite']
        cur.execute("UPDATE articles SET is_favorite=%s WHERE id=%s;", (not current, article_id))
    else:
        cur.execute("SELECT is_favorite FROM articles WHERE id=?;", (article_id,))
        current = cur.fetchone()['is_favorite']
        cur.execute("UPDATE articles SET is_favorite=? WHERE id=?;", (0 if current else 1, article_id))
    db_close(conn, cur)
    return redirect('/lab5/list')
