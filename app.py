from flask import Flask, render_template, request, Response
from db import DatabaseManagement
import management
import ezgmail
import os
import sys

app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')


DEBUG_MODE = os.environ.get('DEBUG_MODE', False)
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
        if email == "Email address":
            return render_template('register.html')
        else:
            return render_template('register.html', status_message="user {} registered successfully".format(email))


@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'GET':
        return render_template("add_customer.html", status_message="")
    else:
        name = request.form.get('customer_name')
        if name == "Customer Name":
            return render_template('add_customer.html')
        else:
            return render_template('add_customer.html', status_message="customer {} added successfully".format(name))


@app.route('/get_users_count', methods=['GET'])
def get_users_count():
    count = db_object.get_users_count()
    return Response(str(count), 200)


@app.route('/get_customers', methods=['GET'])
def get_customers():
    customers = db_object.get_customers()
    return Response(str(customers), 200)


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=DEBUG_MODE)
