from flask import Blueprint, render_template, request, redirect, session, current_app, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path
from db import db
from db.models import users

lab9 = Blueprint("lab9", __name__)

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
        db_path = path.join(path.dirname(path.realpath(__file__)), "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    return conn, cur

def sql_placeholder():
    return "%s" if current_app.config['DB_TYPE'] == "postgres" else "?"

def db_close(conn, cur, commit=True):
    if commit:
        conn.commit()
    cur.close()
    conn.close()

@lab9.route("/lab9/")
def main():
    return render_template(
        "lab9/index.html",
        user_authenticated=current_user.is_authenticated,
        user_login=current_user.login if current_user.is_authenticated else ''
    )

@lab9.route("/lab9/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("lab9/login.html")
    
    login_form = request.form.get("login", "").strip()
    password_form = request.form.get("password", "").strip()

    if not login_form or not password_form:
        return render_template("lab9/login.html", error="Заполните логин и пароль")

    user = users.query.filter_by(login=login_form).first()
    if user and check_password_hash(user.password, password_form):
        login_user(user)
        return redirect("/lab9/")
    return render_template("lab9/login.html", error="Неверный логин или пароль")

@lab9.route("/lab9/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("lab9/register.html")
    
    login_form = request.form.get("login", "").strip()
    password_form = request.form.get("password", "").strip()

    if not login_form or not password_form:
        return render_template("lab9/register.html", error="Заполните все поля")

    if users.query.filter_by(login=login_form).first():
        return render_template("lab9/register.html", error="Пользователь с таким логином уже существует")

    password_hash = generate_password_hash(password_form)
    new_user = users(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)
    return redirect("/lab9/")

@lab9.route("/lab9/logout")
@login_required
def logout():
    logout_user()
    return redirect("/lab9/")

# Подарки
@lab9.route("/lab9/api/gifts")
def api_gifts():
    conn, cur = db_connect()
    cur.execute("SELECT id, top_pos, left_pos, message, opened, gift_image, auth_only FROM gift_boxes ORDER BY id")
    boxes = cur.fetchall()
    db_close(conn, cur, commit=False)

    boxes_list = [dict(b) if isinstance(b, sqlite3.Row) else b for b in boxes]
    user_authenticated = current_user.is_authenticated
    for b in boxes_list:
        if b['auth_only'] and not user_authenticated:
            b['front_image'] = '/static/lab9/locked.jpg'
        else:
            b['front_image'] = '/static/lab9/box.jpg'
    return jsonify(boxes_list)

@lab9.route("/lab9/api/gifts/open/<int:box_id>", methods=["POST"])
def api_gifts_open(box_id):
    if "opened_count" not in session:
        session["opened_count"] = 0
    if session["opened_count"] >= 3:
        return jsonify({"error": "Вы уже открыли 3 коробки!"}), 403

    placeholder = sql_placeholder()
    conn, cur = db_connect()
    cur.execute(f"SELECT * FROM gift_boxes WHERE id={placeholder}", (box_id,))
    box = cur.fetchone()

    if box["opened"]:
        db_close(conn, cur, commit=False)
        return jsonify({"error": "Эта коробка уже открыта"}), 400

    user_authenticated = current_user.is_authenticated
    if box["auth_only"] and not user_authenticated:
        db_close(conn, cur, commit=False)
        return jsonify({"error": "Этот подарок доступен только для авторизованных пользователей!"}), 403

    cur.execute(f"UPDATE gift_boxes SET opened=TRUE WHERE id={placeholder}", (box_id,))
    db_close(conn, cur)
    session["opened_count"] += 1

    return jsonify({
        "message": box["message"],
        "gift_image": "/static/" + box["gift_image"]
    })

@lab9.route("/lab9/api/reset", methods=["POST"])
@login_required
def api_reset_gifts():
    conn, cur = db_connect()
    cur.execute("UPDATE gift_boxes SET opened=FALSE")
    db_close(conn, cur)

    session["opened_count"] = 0

    # После сброса делаем редирект на главную страницу
    return redirect("/lab9/")