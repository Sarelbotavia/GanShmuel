#!flask/bin/python
from flask import Flask, jsonify, render_template, request
from flask_mysqldb import MySQL
import csv
import json
from datetime import datetime
from typing import Optional

app = Flask(__name__)

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123'
app.config['MYSQL_DB'] = 'weight_db'

mysql = MySQL(app)
now=datetime.now()

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


@app.route('/batch-weight', methods=['GET', 'POST'])
def post_batch_weight():
    if request.method == "POST":
        details = request.form
        listfile = details['truck']

        error = 0
        errmsg = "New rows added.\nThe following rows cant be added probably due to uniqe ID already exist:\n"

        if listfile.endswith('.csv'):
            with open('in/' + listfile) as f:
                reader = csv.reader(f)
                data = [tuple(row) for row in reader]

            unit = data[0][1]
            if unit != "lbs" and unit != "kg":
                error = 1
                return "Error! Unknown unit, only LBS and KG are allowed :("

            cur = mysql.connection.cursor()
            for line in data[1:]:
                try:
                    cur.execute(
                        "INSERT INTO containers(id, weight, unit) VALUES (%s, %s, %s)", (line[0], line[1], unit))
                except:
                    error = 1
                    errmsg += line[0]+", "+line[1]+", "+unit+"\n"

            mysql.connection.commit()
            cur.close()

        elif listfile.endswith('.json'):        # need to fix the part of pulling a list from
            with open('in/' + listfile) as f:   # JSON file, right now it prints "u'" before everything
                data = json.load(f)             # and it doesnt put it in a python list, instand it puts it like shit string
                print(data)
                return "this part doesn't work, JSON files SUCK"

        if error == 0:
            return "New rows added! :)"
        elif error == 1:
            return errmsg
    return render_template('batch.html')


@ app.route('/unknown', methods=['GET'])
def get_unknown():
    return "unknown"


@ app.route('/weight?from=t1&to=t2&filter=f', methods=['GET'])
def get_weight_from():
    return "weight?from=t1&to=t2&filter=f"


@app.route('/item/<id>?time=t1&to=t2', methods=['GET'])
def get_item_id(id, t1, t2):
    test_id=id
    first_time=t1
    # second_time=t2

    try:
        cur = mysql.connection.cursor()
    except:
        return "MYSQL_IS_DOWN"
    else:
        # print(first_time)
        # print(second_time)
        query = ("SELECT trucks_id, id, date, bruto FROM sessions WHERE trucks_id='{}';".format(test_id))
        cur.execute(query)
        mysql.connection.commit()
        res = cur.fetchall()
        if not res:
            query = ("SELECT id FROM containers WHERE id='{}';".format(test_id))
            cur.execute(query)
            mysql.connection.commit()
            res = cur.fetchall()
            if not res:
                return "not a valid id"
        cur.close()
        res=first_time
        return jsonify(res)
 

@ app.route('/session/<id>', methods=['GET'])
def get_session():
    return "session/<id>"


@ app.route('/health', methods=['GET'])
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
