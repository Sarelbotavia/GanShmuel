#!flask/bin/python
from flask import Flask, jsonify, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123'
app.config['MYSQL_DB'] = 'weight_db'

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        details = request.form
        firstName = details['fname']
        lastName = details['lname']
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO products(product_name, scope) VALUES (%s, %s)", (firstName, lastName))
        mysql.connection.commit()
        cur.close()
        return 'success'
    return render_template('index.html')


@app.route('/weight', methods=['POST'])
def post_weight():
    return "weight"


@app.route('/batch-weight', methods=['POST'])
def post_batch_weight():
    return "batch-weight"


@app.route('/unknown', methods=['GET'])
def get_unknown():
    return "unknown"


@app.route('/weight?from=t1&to=t2&filter=f', methods=['GET'])
def get_weight_from():
    return "weight?from=t1&to=t2&filter=f"


@app.route('/item/<id>?from=t1&to=t2', methods=['GET'])
def get_item_id():
    return "item/<id>?from=t1&to=t2"


@app.route('/session/<id>', methods=['GET'])
def get_session():
    return "session/<id>"


@app.route('/health', methods=['GET'])
def get_health():
    try:
        cur = mysql.connection.cursor()
    except:
        return "MYSQL_IS_DOWN"
    else:

        cur.close()
        return "RUNNING"

# @app.route('/api/healthy', methods=['GET'])
# def get_tasks():
#     return jsonify({'tasks': tasks})


if __name__ == '__main__':
    app.run()
