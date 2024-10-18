from functools import wraps
from flask import Flask, render_template, request, jsonify, make_response, redirect, url_for, flash

from utils import check_password, decode_token, create_token, hash_password, initial_data
from config import FLASK_SECRET_KEY
from database import get_user_from_db

app = Flask(__name__)
app.config['SECRET_KEY'] = FLASK_SECRET_KEY

def jwt_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.cookies.get('jwt_token')
        if token:
            try:
                current_user = decode_token(token)
                return func(*args, **kwargs)
            
            except Exception as e:
                print(e)
                return redirect(url_for('login'))
        return redirect(url_for('login'))

    return wrapper

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')

        if user:=get_user_from_db(login):
            if check_password(password.encode(), user[2]):
                token = create_token(user[1])
                response = make_response(redirect(url_for('protected_resource')), 200)
                response.set_cookie('jwt_token', token)
                return response
            
            flash('Неверный пароль!')
            return render_template('login.html', title='Авторизация')
        
        flash('Такого пользователя не существует')
    return render_template('login.html', title='Авторизация')

@app.route('/get/login/content')
def login_content():
    return render_template('login_form.html')

@app.route('/protected', methods=['GET'])
#@jwt_required
def protected_resource():
    return render_template('main.html')
    
    
if __name__=='__main__':
    # Заполним пользователями таблицу
    user1 = {
        'id': 1,
        'username': 'admin',
        'password': '1234'
    }
    
    user2 = {
        'id': 2,
        'username': 'user',
        'password': '4321'
    }

    initial_data(user1, user2)

    app.run(host='0.0.0.0', port=5000, debug=False)