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

@lab3.route('/lab3/order_train')
def order_train():
    fio = request.args.get('fio', '')
    berth = request.args.get('berth', '')
    departure = request.args.get('departure', '')
    destination = request.args.get('destination', '')
    date = request.args.get('date', '')
    linen = request.args.get('linen')
    baggage = request.args.get('baggage')
    insurance = request.args.get('insurance')
    
    age_str = request.args.get('age')
    try:
        age = int(age_str)
        if age < 1 or age > 120:
            return "Ошибка: возраст должен быть от 1 до 120 лет."
    except:
        age = None

    price = 0
    services = []

    if age is not None:
        price = 1000 if age >= 18 else 700
        services.append(f"Билет = {price}руб")
        
        if berth in ['нижняя', 'нижняя боковая']:
            price += 100
            services.append("Место: нижнее = 100руб")
        if linen == 'on':
            price += 75
            services.append("Постельное бельё = 75руб")
        if baggage == 'on':
            price += 250
            services.append("Багаж = 250руб")
        if insurance == 'on':
            price += 150
            services.append("Страховка = 150руб")

    return render_template('lab3/order_train.html',
                           fio=fio,
                           berth=berth,
                           departure=departure,
                           destination=destination,
                           date=date,
                           age=age,
                           price=price,
                           services=services)

@lab3.route('/lab3/clear_cookies')
def clear_cookies():
    resp = make_response(redirect('/lab3'))
    cookies_to_clear = ['color', 'background_color', 'font_size', 'font_style']
    for cookie in cookies_to_clear:
        resp.set_cookie(cookie, '')
    return resp

products = [
    {"name": "iPhone 13", "price": 80000, "brand": "Apple", "color": "черный"},
    {"name": "iPhone 12", "price": 60000, "brand": "Apple", "color": "белый"},
    {"name": "Galaxy S22", "price": 70000, "brand": "Samsung", "color": "черный"},
    {"name": "Galaxy S21", "price": 55000, "brand": "Samsung", "color": "синий"},
    {"name": "Xiaomi Mi 11", "price": 40000, "brand": "Xiaomi", "color": "черный"},
    {"name": "Xiaomi Mi 10", "price": 30000, "brand": "Xiaomi", "color": "белый"},
    {"name": "Redmi Note 10", "price": 20000, "brand": "Xiaomi", "color": "синий"},
    {"name": "Pixel 6", "price": 65000, "brand": "Google", "color": "черный"},
    {"name": "Pixel 5", "price": 50000, "brand": "Google", "color": "зеленый"},
    {"name": "OnePlus 9", "price": 45000, "brand": "OnePlus", "color": "черный"},
    {"name": "OnePlus 8", "price": 35000, "brand": "OnePlus", "color": "красный"},
    {"name": "Sony Xperia 5", "price": 60000, "brand": "Sony", "color": "черный"},
    {"name": "Sony Xperia 1", "price": 70000, "brand": "Sony", "color": "белый"},
    {"name": "Huawei P40", "price": 50000, "brand": "Huawei", "color": "черный"},
    {"name": "Huawei P30", "price": 35000, "brand": "Huawei", "color": "синий"},
    {"name": "Nokia 8.3", "price": 25000, "brand": "Nokia", "color": "черный"},
    {"name": "Nokia 5.4", "price": 15000, "brand": "Nokia", "color": "синий"},
    {"name": "Motorola Edge", "price": 40000, "brand": "Motorola", "color": "черный"},
    {"name": "Motorola G9", "price": 20000, "brand": "Motorola", "color": "зеленый"},
    {"name": "Realme 8", "price": 18000, "brand": "Realme", "color": "белый"}
]

@lab3.route('/lab3/products')
def products_page():
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')

    cookie_min = request.cookies.get('min_price')
    cookie_max = request.cookies.get('max_price')

    if not min_price and cookie_min:
        min_price = cookie_min
    if not max_price and cookie_max:
        max_price = cookie_max

    if min_price:
        min_price_val = int(min_price)
    else:
        min_price_val = None

    if max_price:
        max_price_val = int(max_price)
    else:
        max_price_val = None


    #Корректируем если min > max
    if min_price_val and max_price_val and min_price_val > max_price_val:
        min_price_val, max_price_val = max_price_val, min_price_val

    filtered = []
    for p in products:
        if min_price_val != None and p['price'] < min_price_val:
            continue
        if max_price_val != None and p['price'] > max_price_val:
            continue
        filtered.append(p)

    resp = make_response(render_template(
        'products.html',
        products=filtered,
        count=len(filtered),
        min_price=min_price_val,
        max_price=max_price_val,
        global_min=min([p['price'] for p in products]),
        global_max=max([p['price'] for p in products])
    ))

    if min_price_val != None:
        resp.set_cookie('min_price', str(min_price_val))
    if max_price_val != None:
        resp.set_cookie('max_price', str(max_price_val))
    return resp

@lab3.route('/lab3/products/reset')
def reset_products():
    resp = make_response(redirect('/lab3/products'))
    resp.set_cookie('min_price', '')
    resp.set_cookie('max_price', '')
    return resp