from flask import Flask, render_template, request, Response
from db import DatabaseManagement
from passlib.hash import sha256_crypt
import passwordValidator
import os

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')

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
        # if email == "Email address":
       # mail = request.form['mail']
        print(email)
        check = db_object.get_specific_user_by_email(email)
        if check:
            #    hashCode = ''.join(random.choices(string.ascii_letters + string.digits, k=24))
            #    check.hashCode = hashCode
            #    db.session.commit()
            #    msg = Message('Confirm Password Change', sender='berat@github.com', recipients=[mail])
            #    msg.body = "Hello,\nWe've received a request to reset your password. If you want to reset your password, click the link below and enter your new password\n http://localhost:5000/" + check.hashCode
            #    posta.send(msg)
            #    return '''
            #                <form action="/" method="post">
            #                    <small>enter the email address of the account you forgot your password</small> <br>
            #                    <input type="email" name="mail" id="mail" placeholder="mail@mail.com"> <br>
            #                    <input type="submit" value="Submit">
            #                </form>
            #            '''
            # else:
            #    return '''
            #            <form action="/" method="post">
            #                <small>enter the email address of the account you forgot your password</small> <br>
            #                <input type="email" name="mail" id="mail" placeholder="mail@mail.com"> <br>
            #                <input type="submit" value="Submit">
            #            </form>
            #        '''
            print(check)
            return render_template("forgot_password.html", status_message="check email")
        else:
            return render_template("forgot_password.html", status_message="given address not registered")
        #check = User.query.filter_by(mail=mail).first()


#    return render_template('register.html')
# else:
#    return render_template('register.html', status_message="user {} registered successfully".format(email))


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=DEBUG_MODE)
