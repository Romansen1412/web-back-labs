import os
import re
import datetime
from functools import wraps
from flask import Blueprint, render_template, session, request, redirect, url_for, current_app, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor

#  Подключение к БД 
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
        dir_path = os.path.dirname(os.path.realpath(__file__))
        db_path = os.path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

#  Blueprint 
template_dir = os.path.join(os.path.dirname(__file__), 'templates', 'rgz')
rgz = Blueprint('rgz', __name__, template_folder=template_dir)

#  Валидация логина/пароля 
ALLOWED_LOGIN_RE = re.compile(
    r'^[A-Za-z0-9' + re.escape(r"""!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~""") + r']+$'
)

def valid_login_or_password(s: str) -> bool:
    return bool(s and ALLOWED_LOGIN_RE.fullmatch(s))

#  Универсальный placeholder для SQL
def _get_placeholder():
    return '%s' if current_app.config.get('DB_TYPE') == 'postgres' else '?'

def db_execute(query, params=(), fetchone=False, fetchall=False, commit=False):
    conn, cur = db_connect()
    try:
        placeholder = _get_placeholder()
        query_fixed = query.replace('{p}', placeholder)
        cur.execute(query_fixed, params)
        if fetchone:
            return cur.fetchone()
        if fetchall:
            return cur.fetchall()
        if commit:
            conn.commit()
    finally:
        db_close(conn, cur)

#  Аутентификация 
def get_current_user():
    user_id = session.get('user_id')
    if not user_id:
        return None
    row = db_execute("SELECT id, name, login FROM users2 WHERE id = {p}", (user_id,), fetchone=True)
    return dict(row) if row else None

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not get_current_user():
            return redirect(url_for('rgz.login', next=request.path))
        return func(*args, **kwargs)
    return wrapper

#  Работа с неделями года 
def weeks_in_year(year: int):
    last_week = datetime.date(year, 12, 28).isocalendar()[1]
    weeks = []
    for w in range(1, last_week + 1):
        try:
            monday = datetime.date.fromisocalendar(year, w, 1)
            sunday = datetime.date.fromisocalendar(year, w, 7)
        except ValueError:
            continue
        weeks.append((w, monday, sunday))
    return weeks

#  Основная страница 
@rgz.route('/rgz/')
def index():
    user = get_current_user()
    try:
        year = int(request.args.get('year', datetime.date.today().year))
    except (ValueError, TypeError):
        year = datetime.date.today().year

    weeks = weeks_in_year(year)
    rows = db_execute("SELECT id, user_id, week_number FROM vacations2 WHERE year = {p}", (year,), fetchall=True)
    taken = {r['week_number']: dict(r) for r in rows} if rows else {}

    user_ids = list({v['user_id'] for v in taken.values()}) if taken else []
    users_map = {}
    if user_ids:
        placeholder = _get_placeholder()
        placeholders = ','.join([placeholder]*len(user_ids))
        sql = f"SELECT id, name FROM users2 WHERE id IN ({placeholders})"
        rows_users = db_execute(sql, tuple(user_ids), fetchall=True)
        users_map = {ru['id']: ru['name'] for ru in rows_users}

    marked_weeks = []
    marked_count = 0
    if user:
        mu_rows = db_execute(
            "SELECT week_number FROM vacations2 WHERE year = {p} AND user_id = {p}",
            (year, user['id']), fetchall=True
        )
        marked_weeks = [r['week_number'] for r in mu_rows] if mu_rows else []
        marked_count = len(marked_weeks)

    current_year = datetime.date.today().year
    editable = year >= current_year
    missing = 4 - marked_count if user and marked_count < 4 else None

    employees_count_row = db_execute("SELECT COUNT(*) as cnt FROM users2", (), fetchone=True)
    employees_count = employees_count_row['cnt'] if employees_count_row else 0

    return render_template(
        'index.html',
        user=user,
        year=year,
        weeks=weeks,
        taken=taken,
        users_map=users_map,
        marked_weeks=marked_weeks,
        marked_count=marked_count,
        editable=editable,
        missing=missing,
        employees_count=employees_count
    )

#  Вход 
@rgz.route('/rgz/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', next=request.args.get('next', ''))
    login_form = request.form.get('login', '').strip()
    password_form = request.form.get('password', '').strip()
    next_url = request.form.get('next', '').strip()

    if not login_form or not password_form:
        flash("Заполните логин и пароль", "error")
        return render_template('login.html', next=next_url)

    if not valid_login_or_password(login_form):
        flash("Неверный формат логина", "error")
        return render_template('login.html', next=next_url)

    user_row = db_execute(
        "SELECT id, login, password, name FROM users2 WHERE login = {p}",
        (login_form,), fetchone=True
    )
    if user_row and check_password_hash(user_row['password'], password_form):
        session['user_id'] = user_row['id']
        session['login'] = user_row['login']
        flash(f"Добро пожаловать, {user_row['name']}!", "success")
        return redirect(next_url or url_for('rgz.index'))

    flash("Неверный логин или пароль", "error")
    return render_template('login.html', next=next_url)

#  Регистрация 
@rgz.route('/rgz/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    name = request.form.get('name', '').strip()
    login_form = request.form.get('login', '').strip()
    password_form = request.form.get('password', '').strip()

    if not name or not login_form or not password_form:
        flash("Заполните все поля", "error")
        return render_template('register.html', name=name, login=login_form)

    if not valid_login_or_password(login_form):
        flash("Логин содержит недопустимые символы", "error")
        return render_template('register.html', name=name, login=login_form)
    if not valid_login_or_password(password_form):
        flash("Пароль содержит недопустимые символы", "error")
        return render_template('register.html', name=name, login=login_form)

    exists = db_execute("SELECT id FROM users2 WHERE login = {p}", (login_form,), fetchone=True)
    if exists:
        flash("Пользователь с таким логином уже существует", "error")
        return render_template('register.html', name=name, login=login_form)

    password_hash = generate_password_hash(password_form)
    db_execute(
        "INSERT INTO users2 (name, login, password) VALUES ({p}, {p}, {p})",
        (name, login_form, password_hash),
        commit=True
    )

    user_row = db_execute("SELECT id, login FROM users2 WHERE login = {p}", (login_form,), fetchone=True)
    session['user_id'] = user_row['id']
    session['login'] = user_row['login']
    flash(f"Пользователь {name} зарегистрирован успешно!", "success")
    return redirect(url_for('rgz.index'))

#  Выход 
@rgz.route('/rgz/logout')
def logout():
    session.pop('user_id', None)
    session.pop('login', None)
    flash("Вы вышли из системы.", "info")
    return redirect(url_for('rgz.index'))

#  Удаление аккаунта 
@rgz.route('/rgz/delete_account', methods=['POST'])
@login_required
def delete_account():
    user = get_current_user()
    db_execute("DELETE FROM vacations2 WHERE user_id = {p}", (user['id'],), commit=True)
    db_execute("DELETE FROM users2 WHERE id = {p}", (user['id'],), commit=True)
    session.clear()
    flash("Ваш аккаунт удалён.", "info")
    return redirect(url_for('rgz.index'))

#  Пометка/снятие отпуска 
@rgz.route('/rgz/toggle/<int:year>/<int:week_number>', methods=['POST'])
@login_required
def toggle_week(year, week_number):
    user = get_current_user()
    current_year = datetime.date.today().year
    if year < current_year:
        flash("Прошлые годы только для просмотра.", "error")
        return redirect(url_for('rgz.index', year=year))

    weeks = weeks_in_year(year)
    if week_number not in {w[0] for w in weeks}:
        flash("Неверный номер недели.", "error")
        return redirect(url_for('rgz.index', year=year))

    occ = db_execute(
        "SELECT id, user_id FROM vacations2 WHERE year = {p} AND week_number = {p}",
        (year, week_number), fetchone=True
    )
    if occ:
        occ = dict(occ)
        if occ['user_id'] == user['id']:
            db_execute("DELETE FROM vacations2 WHERE id = {p}", (occ['id'],), commit=True)
            flash(f"Неделя {week_number} снята с вашего отпуска.", "info")
        else:
            other = db_execute("SELECT name FROM users2 WHERE id = {p}", (occ['user_id'],), fetchone=True)
            other_name = other['name'] if other else "другой сотрудник"
            flash(f"Эта неделя уже занята ({other_name}).", "error")
    else:
        cnt_row = db_execute(
            "SELECT COUNT(*) as cnt FROM vacations2 WHERE year = {p} AND user_id = {p}",
            (year, user['id']), fetchone=True
        )
        cnt = cnt_row['cnt'] if cnt_row else 0
        if cnt >= 4:
            flash("Нельзя пометить больше 4 недель.", "error")
        else:
            monday = datetime.date.fromisocalendar(year, week_number, 1)
            sunday = datetime.date.fromisocalendar(year, week_number, 7)
            db_execute(
                "INSERT INTO vacations2 (user_id, year, week_number, date_from, date_to) VALUES ({p}, {p}, {p}, {p}, {p})",
                (user['id'], year, week_number, monday.isoformat(), sunday.isoformat()),
                commit=True
            )
            flash(f"Неделя {week_number} ({monday} — {sunday}) помечена как отпуск.", "success")
    return redirect(url_for('rgz.index', year=year))