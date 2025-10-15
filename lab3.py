from flask import Blueprint, render_template, request, make_response, redirect
lab3 = Blueprint('lab3', __name__, template_folder='templates/lab3')

@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name') or "Аноним"
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age') or "Неизвестно"
    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)

@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp

@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp

@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'
    age = request.args.get('age')
    if age == '':
        errors['age'] = 'Заполните поле!'
    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)

@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')

@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    # Кофе стоит 120 рублей, чёрный чай - 80 рублей, зелёный - 70 рублей.
    if drink == 'cofee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70
    # Добавка молока + 30 рублей, а сахара + 10.
    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10
    return render_template('lab3/pay.html', price=price)

@lab3.route('/lab3/success')
def success():
    price = request.args.get('price')
    drink = request.args.get('drink')
    milk = request.args.get('milk')
    sugar = request.args.get('sugar')

    if drink == 'cofee':
        drink_name = 'Кофе = 120руб'
    elif drink == 'black-tea':
        drink_name = 'Чёрный чай = 80руб'
    else:
        drink_name = 'Зелёный чай = 70руб'

    additions = []
    if milk == 'on':
        additions.append('Молоко = 30руб')
    if sugar == 'on':
        additions.append('Сахар = 10руб')

    return render_template('lab3/success.html', price=price, drink_name=drink_name, additions=additions)

@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    background_color = request.args.get('background_color')
    font_size = request.args.get('font_size')
    font_style = request.args.get('font_style')

    if color or background_color or font_size or font_style:
        resp = make_response(redirect('/lab3/settings'))
        if color:
            resp.set_cookie('color', color)
        if background_color:
            resp.set_cookie('background_color', background_color)
        if font_size:
            resp.set_cookie('font_size', font_size)
        if font_style:
            resp.set_cookie('font_style', font_style)
        return resp

    color = request.cookies.get('color')
    background_color = request.cookies.get('background_color')
    font_size = request.cookies.get('font_size')
    font_style = request.cookies.get('font_style')
    resp = make_response(render_template(
        'lab3/settings.html',
        color=color,
        background_color=background_color,
        font_size=font_size,
        font_style=font_style
    ))
    return resp
