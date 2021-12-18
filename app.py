from flask import Flask, render_template, request, Response
from db import DatabaseManagement
from passlib.hash import sha256_crypt
import passwordValidator
import os
import random
import string
from flask_mail import Mail, Message

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')

MAIL_USERNAME = os.environ.get('MAIL_USER')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
# app.secret_key = 'some_secret'
mail_object = Mail(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/bozkurt/Desktop/forgot-password/database.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

DEBUG_MODE = os.environ.get('DEBUG_MODE', False)
HASH_SALT = os.environ.get('HASH_SALT')
db_object = DatabaseManagement()


@app.route('/', methods=['GET'])
def homepage():
    customers = db_object.get_customers()
    return render_template("index.html", customers=customers)


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
            res = db_object.get_user_password(email)
            stored_password = res[0][0]
            is_locked = res[0][1]

            if is_locked:
                return render_template('login.html', status_message="Your user is locked, please contact administrator")

            if sha256_crypt.verify(password + HASH_SALT, stored_password):
                return render_template('login.html', status_message="Login successful")
            else:
                return render_template('login.html', status_message="Login failed")


@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'GET':
        return render_template("add_customer.html", status_message="")
    else:
        name = request.form.get('customer_name')
        address = request.form.get('address')
        phone = request.form.get('phone')
        if name == "" or address == "" or phone == "":
            return render_template('add_customer.html',
                                   status_message="Make sure to fill all fields")
        else:
            db_object.insert_customer(name, address, phone)
            return render_template('add_customer.html', status_message="Customer {} added successfully".format(name))


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'GET':
        return render_template("forgot_password.html", status_message="")
    else:
        email = request.form.get('email')
        check = db_object.get_specific_user_by_email(email)
        if check:
            random_password = ''.join(random.choices(string.ascii_letters + string.digits, k=24))
            msg = Message('Confirm Password Change', sender=MAIL_USERNAME, recipients=[email])
            msg.body = "Hello,\nWe've received a request to reset your password." \
                       "\nThis is your new generated password: " + random_password
            mail_object.send(msg)
            password_hashed = sha256_crypt.encrypt(random_password + HASH_SALT)
            db_object.update_user(email, password_hashed, 1)
            return render_template("forgot_password.html", status_message="check email")
        else:
            return render_template("forgot_password.html", status_message="given address not registered")


@app.route('/change_password', methods=['GET', 'POST'])
def change_passowrd():
    if request.method == 'GET':
        return render_template('change_password.html')
    else:
        email = request.form.get('email')
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        repeat_new_password = request.form.get('repeat_new_password')
        if new_password != repeat_new_password:
            return render_template('change_password.html', status_message="New Password and Repeat New Password are not"
                                                                          " equal, please try again")

        if old_password == "" or new_password == "" or repeat_new_password == "":
            return render_template('change_password.html', status_message="Make sure to fill all fields")

        res = db_object.get_user_password(email)
        stored_password = res[0][0]
        is_locked = res[0][1]

        if is_locked:
            return render_template('change_password.html', status_message="Your user is locked, please contact administrator")

        if sha256_crypt.verify(old_password + HASH_SALT, stored_password):
            password_hashed = sha256_crypt.encrypt(new_password + HASH_SALT)
            db_object.update_user(email, password_hashed, 0)
            return render_template('change_password.html', status_message="Change password succeeded")
        else:
            return render_template('change_password.html', status_message="Change password failed")


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=DEBUG_MODE)
