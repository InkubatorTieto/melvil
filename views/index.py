from flask import render_template, request, session
from . import library
from models.user import User


@library.route('/')
def index():
    return render_template('index.html')


@library.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        print("To ja")
        email = request.form['email']
        passw = request.form['password']
        try:
            data = User.query.filter_by(email=email, password_hash=passw).first()
            print(data)

            if data is not None:
                print(data)
                session['logged_in'] = True
                print("Sesja się udała")
                return render_template('index.html')

            else:
                return 'Login failed'
        except:
            return "Login failed"
