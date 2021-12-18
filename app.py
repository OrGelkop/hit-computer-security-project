from flask import Flask, render_template, request, url_for
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.utils import redirect

from db import DatabaseManagement
from passlib.hash import sha256_crypt
from user import User
import passwordValidator
import os


DEBUG_MODE = os.environ.get('DEBUG_MODE', False)
HASH_SALT = os.environ.get('HASH_SALT')

app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')

login_manager = LoginManager()
login_manager.init_app(app)
db_object = DatabaseManagement()


@login_manager.user_loader
def load_user(uid):
    email = db_object.get_user_by_uid(uid)[0][0]
    is_active = True
    return User(uid, email, is_active)


@app.route('/', methods=['GET'])
def homepage():
    customers = db_object.get_customers()
    print(type(current_user))
    print(current_user)
    return render_template("index.html", customers=customers, logged_user=current_user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html", status_message="")
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        if email == "" or password == "":
            return render_template('register.html', status_message="Make sure to fill all fields")
        else:
            validate_password_resp = passwordValidator.validate_password(password)
            if not validate_password_resp['status']:
                return render_template('register.html', status_message=validate_password_resp['info'])

            password_hashed = sha256_crypt.encrypt(password + HASH_SALT)
            db_object.insert_user(email, password_hashed)
            return render_template('register.html', status_message="User {} registered successfully".format(email))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        if email == "" or password == "":
            return render_template('login.html', status_message="Make sure to fill all fields")
        else:
            res = db_object.get_user_by_email(email)
            user_id = res[0][0]
            stored_password = res[0][1]
            is_locked = res[0][2]

            if is_locked:
                return render_template('login.html', status_message="Your user is locked, please contact administrator")

            if sha256_crypt.verify(password + HASH_SALT, stored_password):
                login_user(User(user_id, email, password))
                return render_template('login.html', status_message="Login successful")
            else:
                return render_template('login.html', status_message="Login failed")


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('homepage'))


@app.route('/add_customer', methods=['GET', 'POST'])
@login_required
def add_customer():
    if request.method == 'GET':
        return render_template("add_customer.html", status_message="")
    else:
        name = request.form.get('customer_name')
        address = request.form.get('address')
        phone = request.form.get('phone')
        if name == "" or address == "" or phone == "":
            return render_template('add_customer.html', status_message="Make sure to fill all fields")
        else:
            db_object.insert_customer(name, address, phone)
            return render_template('add_customer.html', status_message="Customer {} added successfully".format(name))


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    return "test"


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=DEBUG_MODE)
