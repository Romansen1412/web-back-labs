from flask import Blueprint, render_template, session, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from db.models import users, articles
from flask_login import login_user, logout_user, login_required, current_user

lab8 = Blueprint("lab8", __name__)

@lab8.route('/lab8/')
def main():
    return render_template('lab8/lab8.html', login = current_user.login if current_user.is_authenticated else 'anonymous')

@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')

    login_form = request.form.get('login', '').strip()
    password_form = request.form.get('password', '').strip()
    remember_me = bool(request.form.get('remember'))

    if not login_form or not password_form:
        return render_template('lab8/login.html', error="Заполните логин и пароль")

    user = users.query.filter_by(login=login_form).first()

    if user and check_password_hash(user.password, password_form):
        # передаем параметр remember из формы
        login_user(user, remember=remember_me)
        session['login'] = user.login
        return redirect('/lab8/')

    return render_template('lab8/login.html', error="Неверный логин или пароль")

@lab8.route('/lab8/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')

    login_form = request.form.get('login', '').strip()
    password_form = request.form.get('password', '').strip()

    if not login_form or not password_form:
        return render_template('lab8/register.html', error="Заполните все поля")

    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('lab8/register.html', error="Пользователь с таким логином уже существует")
    
    password_hash = generate_password_hash(password_form)
    new_user = users(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user, remember=False)
    session['login'] = new_user.login
    
    return redirect('/lab8/')

@lab8.route('/lab8/articles')
def list_articles():
    if current_user.is_authenticated:
        # публичные статьи + свои
        articles_list = articles.query.filter(
            (articles.is_public == True) | (articles.login_id == current_user.id)
        ).all()
    else:
        # только публичные
        articles_list = articles.query.filter_by(is_public=True).all()
    return render_template('lab8/articles.html', articles=articles_list)

@lab8.route('/lab8/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'GET':
        return render_template('lab8/create_article.html')

    title = request.form.get('title', '').strip()
    article_text = request.form.get('article_text', '').strip()
    is_public = bool(request.form.get('is_public'))

    if not title or not article_text:
        return render_template('lab8/create_article.html', 
                               error="Заполните все поля", 
                               title=title, article_text=article_text, is_public=is_public)

    new_article = articles(
        login_id=current_user.id,
        title=title,
        article_text=article_text,
        is_public=is_public,
        is_favorite=False,
        likes=0
    )
    db.session.add(new_article)
    db.session.commit()
    return redirect('/lab8/articles')

@lab8.route('/lab8/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = articles.query.filter_by(id=article_id, login_id=current_user.id).first()
    if not article:
        return "У вас нет прав на редактирование этой статьи", 403

    if request.method == 'GET':
        return render_template('lab8/edit_article.html', article=article)

    title = request.form.get('title', '').strip()
    article_text = request.form.get('article_text', '').strip()

    if not title or not article_text:
        return render_template('lab8/edit_article.html', article=article, 
                               error="Поля не могут быть пустыми")

    article.title = title
    article.article_text = article_text
    db.session.commit()
    return redirect('/lab8/articles')

@lab8.route('/lab8/delete/<int:article_id>', methods=['POST'])
@login_required
def delete_article(article_id):
    article = articles.query.filter_by(id=article_id, login_id=current_user.id).first()
    if not article:
        return "У вас нет прав на удаление этой статьи", 403

    db.session.delete(article)
    db.session.commit()
    return redirect('/lab8/articles')

@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')
