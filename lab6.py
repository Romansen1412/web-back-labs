from flask import Blueprint, render_template, request, session

lab6 = Blueprint('lab6', __name__)

offices = []
for i in range(1, 11):
    offices.append({"number": i, "tenant": "", "price": 900 + i*3}) # tenant пустой - офис свободен

@lab6.route('/lab6/')
def main():
    return render_template('lab6/lab6.html')

@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    id = data['id']
    
    # список офисов
    if data['method'] == 'info':
        return {
            'jsonrpc': '2.0',
            'result': offices,
            'id': id
        }

    # бронирование офиса
    elif data['method'] == 'booking':
        login = session.get('login')
        if not login:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 1,
                    'message': 'Unauthorized'
                },
                'id': id
            }

        office_number = data['params']  # номер офиса для бронирования
        for office in offices:
            if office['number'] == office_number:
                if office['tenant'] != '':
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 2,
                            'message': 'Already booked'
                        },
                        'id': id
                    }
                # Бронируем офис
                office['tenant'] = login
                return {
                    'jsonrpc': '2.0',
                    'result': 'success',
                    'id': id
                }

    # снятие брони с офиса
    elif data['method'] == 'cancellation':
        login = session.get('login')
        if not login:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 1,
                    'message': 'Unauthorized'
                },
                'id': id
            }

        office_number = data['params']
        for office in offices:
            if office['number'] == office_number:
                if office['tenant'] == '':
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 3,
                            'message': 'Office is not booked'
                        },
                        'id': id
                    }
                # Если офис не равен твоему логину - нельзя
                if office['tenant'] != login:
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 4,
                            'message': 'Cannot cancel someone else\'s booking'
                        },
                        'id': id
                    }
                # Снимаем бронь
                office['tenant'] = ''
                return {
                    'jsonrpc': '2.0',
                    'result': 'success',
                    'id': id
                }

    return {
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'message': 'Method not found'
        },
        'id': id
    }
