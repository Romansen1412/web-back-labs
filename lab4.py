from flask import Blueprint, render_template, request, redirect, session
lab4 = Blueprint('lab4', __name__)

@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')

@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')

@lab4.route('/lab4/div', methods = ['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены')
    elif x2 == '0':
        return render_template('lab4/div.html', error='На ноль делить нельзя!')
    else:
        x1 = int(x1)
        x2 = int(x2)
        result = x1 / x2
        return render_template('lab4/div.html', x1=x1, x2=x2, result=result)
    
@lab4.route('/lab4/sum', methods=['POST'])
def summn():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if x1 == '':
        x1 = 0
    if x2 == '':
        x2 = 0

    x1 = int(x1)
    x2 = int(x2)
    result = x1 + x2
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/mul', methods=['POST'])
def multiply():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if x1 == '':
        x1 = 1
    if x2 == '':
        x2 = 1

    x1 = int(x1)
    x2 = int(x2)
    result = x1 * x2
    return render_template('lab4/mul.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/sub', methods=['POST'])
def subtract():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if x1 == '' or x2 == '':
        return render_template('lab4/sub.html', error='Оба поля должны быть заполнены')
    else:
        x1 = int(x1)
        x2 = int(x2)
        result = x1 - x2
        return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/pow', methods=['POST'])
def power():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if x1 == '' or x2 == '':
        return render_template('lab4/pow.html', error='Оба поля должны быть заполнены')

    x1 = int(x1)
    x2 = int(x2)

    if x1 == 0 and x2 == 0:
        return render_template('lab4/pow.html', error='0 в степени 0 не имеет смысла!')
    else:
        result = x1 ** x2
        return render_template('lab4/pow.html', x1=x1, x2=x2, result=result)

tree_count = 0

@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count)

    operation = request.form.get('operation')

    if operation == 'plant':
        tree_count += 1
    elif operation == 'cut' and tree_count > 0:
        tree_count -= 1

    return redirect('/lab4/tree')

users = [
    {'login': 'alex', 'password': '123', 'name': 'Алексей Иванов', 'gender': 'male'},
    {'login': 'bob', 'password': '555', 'name': 'Боб Бобов', 'gender': 'male'},
    {'login': 'roman', 'password': '999', 'name': 'Роман Алексеевич', 'gender': 'male'},
    {'login': 'alina', 'password': '321', 'name': 'Алина Александровна', 'gender': 'female'},
    {'login': 'admin', 'password': 'admin', 'name': 'Администратор. Я в вашем распоряжении', 'gender': 'male'}
]

@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            login = session['login']
            user = None
            for u in users:
                if u['login'] == login:
                    user = u
            name = user['name'] if user else login
        else:
            authorized = False
            login = ''
            name = ''
        return render_template('lab4/login.html', login=login, authorized=authorized, name=name)

    login = request.form.get('login')
    password = request.form.get('password')

    if not login:
        return render_template('lab4/login.html', error='Не введён логин', authorized=False, login=login)
    if not password:
        return render_template('lab4/login.html', error='Не введён пароль', authorized=False, login=login)

    for user in users:
        if login == user['login'] and password == user['password']:
            session['login'] = login
            return redirect('/lab4/login')

    error = 'Неверные логин и/или пароль'
    return render_template('lab4/login.html', error=error, authorized=False, login=login)

@lab4.route('/lab4/logout', methods = ['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')

@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    message = ''
    snowflakes = 0
    temperature = None

    if request.method == 'POST':
        temp_input = request.form.get('temperature')

        if not temp_input:
            message = 'Ошибка: не задана температура'
        else:
            try:
                temperature = float(temp_input)

                if temperature < -12:
                    message = 'Не удалось установить температуру — слишком низкое значение'
                elif temperature > -1:
                    message = 'Не удалось установить температуру — слишком высокое значение'
                elif -12 <= temperature <= -9:
                    message = f'Установлена температура: {temperature}°С'
                    snowflakes = 3
                elif -8 <= temperature <= -5:
                    message = f'Установлена температура: {temperature}°С'
                    snowflakes = 2
                elif -4 <= temperature <= -1:
                    message = f'Установлена температура: {temperature}°С'
                    snowflakes = 1
            except ValueError:
                message = 'Ошибка: введено некорректное значение'

    return render_template('/lab4/fridge.html', message=message, snowflakes=snowflakes, temperature=temperature)