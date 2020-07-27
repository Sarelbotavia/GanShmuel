#!flask/bin/python
from flask import Flask, jsonify
from flask import render_template
from flask import request
from flask_mysqldb import MySQL
# from config import Config
# from flask_migrate import Migrate
# from flask_sqlalchemy import SQLAlchemy
# connections
app = Flask(_name_)

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'qwerty'
app.config['MYSQL_DB'] = 'information_schema'

mysql = MySQL(app)

#db = MySQL.connect("localhost", "root", "qwerty", "information_schema")


# =================================================================


# Routing:

@app.route('/')
def index():
    return "Hello, World!"


@app.route('/health', methods=['GET'])
def check_health():
    query = "SELECT * FROM PLUGINS;"
    cur = mysql.connection.cursor()
    cur.execute(query)
    mysql.connection.commit()
    res = cur.fetchall()
    cur.close()
    return jsonify(res)


@app.route('/provider/reg', methods=['POST'])
def get_tasks():
    name = request.form.get("p_name")
    return name


@app.route('/provider/add', methods=['GET'])
def load_form():
    return render_template('index.html')


# @app.route('/api/healthy', methods=['GET'])
# def get_tasks():
#     return jsonify({'tasks': tasks})


@app.route('/provider/{id}', methods=['PUT'])
def update_provider():
    return "return render_template('index.html')"

@app.route('/rates', methods=['POST'])
def upload_rates():
    return "return render_template('index.html')"

@app.route('/rates', methods=['GET'])
def get_rates():
    return "return render_template('index.html')"

@app.route('/truck', methods=['POST'])
def add_truck():
    return "return render_template('index.html')"

@app.route('/truck/{id}', methods=['PUT'])
def update_truck():
    return "return render_template('index.html')"

@app.route('/truck/<id>?from=t1&to=t2', methods=['GET'])
def get_truck():
    return "return render_template('index.html')"

@app.route('/bill/<id>?from=t1&to=t2', methods=['GET'])
def get_bill():
    return "return render_template('index.html')"

@app.route('/health', methods=['GET'])
def get_health():
    return "return render_template('index.html')"

# @app.route('/api/healthy', methods=['GET'])
# def get_tasks():
#     return jsonify({'tasks': tasks})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port="5000")
