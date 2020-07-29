#!/usr/bin/env python3
import os,random,shutil
import pandas as pd
from flask import Flask, jsonify,send_file
from flask import render_template
from flask import request
import requests
import json
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename

# from config import Config
# from flask_migrate import Migrate
# from flask_sqlalchemy import SQLAlchemy
# connections

# eviroment variables
LAST_UPLOADED_EXCEL="/tmp/last_excel.xlsx"
ALLOWED_EXTENSIONS = {'xlsx','xls'}
project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, './templates')
app = Flask(__name__, template_folder=template_path)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_HOST'] = 'Blue.develeap.com'
app.config['MYSQL_USER'] = 'provider'
app.config['MYSQL_PASSWORD'] = '123'
app.config['MYSQL_DB'] = 'billdb'
app.config['MYSQL_PORT'] = 8086

mysql = MySQL(app)

#db = MySQL.connect("localhost", "root", "qwerty", "information_schema")


# =================================================================

# Global methods :

def get(url):
    try:
        res = requests.get(url)
        return jsonify(res.json())
    except:
        return "cant connect to the api"

# ====================================================================


# Routing:

@app.route('/')
def index():
    return "Hello, World!"


@app.route('/provider/reg', methods=['POST'])
def get_tasks():
    providerName = request.form.get("p_name")
    query = "INSERT INTO Provider (name) VALUES ('{}')".format(providerName)
    cur = mysql.connection.cursor()
    cur.execute(query)
    mysql.connection.commit()
    query = "SELECT * FROM Provider WHERE name=('{}')".format(providerName)
    cur = mysql.connection.cursor()
    cur.execute(query)
    mysql.connection.commit()
    res = cur.fetchall()
    cur.close()
    return jsonify(res)
    # INSERT INTO table_name
    #VALUES (value1, value2, value3, ...);


@app.route('/provider/add', methods=['GET'])
def load_form():
    return render_template('index.html')


@app.route('/provider/{id}', methods=['PUT'])
def update_provider():
    return "return render_template('index.html')"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_safe_temp_filename(base_name_to_use):
    base_name_to_use = "flask_tmp_file_" + str(random.randint(10000000000,99999999999)) + "_" + secure_filename(base_name_to_use)
    return os.path.join("/tmp", base_name_to_use)

def mysql_execute_query(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    mysql.connection.commit()

@app.route('/rates/reg', methods=['POST'])
def upload_rates():
    files_to_delete_when_function_finishes = []
    try:
        f = request.files['file']
        #checkfile
        if ( not allowed_file(f.filename)):
            return "not an excel file : try again"

        #save excel file to disk
        excel_file_temp_path = get_safe_temp_filename(f.filename)
        f.save(excel_file_temp_path)
        files_to_delete_when_function_finishes.append(excel_file_temp_path)

        #convert to csv
        csv_file_temp_path = get_safe_temp_filename("newfile.csv")
        excel_to_csv=pd.read_excel(excel_file_temp_path)
        excel_to_csv.to_csv(csv_file_temp_path,index = None, header=True)
        files_to_delete_when_function_finishes.append(csv_file_temp_path)

        #insetr into database
        query = "DELETE FROM Rates "
        mysql_execute_query(query)

        query = """LOAD DATA LOCAL INFILE '{}' INTO TABLE Rates FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS """
        query=query.format(csv_file_temp_path)
        mysql_execute_query(query)

        query = "SELECT * FROM Rates "
        cur = mysql.connection.cursor()
        cur.execute(query)
        res = cur.fetchall()
        cur.close()

        #save last file
        if os.path.isfile(LAST_UPLOADED_EXCEL):
            os.remove(LAST_UPLOADED_EXCEL)
        shutil.copy(excel_file_temp_path,LAST_UPLOADED_EXCEL)
        return jsonify(res)

    except:
        return 'Somthing went wrong, try again :)'
        
    finally:
        for x in files_to_delete_when_function_finishes:
            if os.path.isfile(x):
                os.remove(x)

    
@app.route('/rates/add', methods=['GET'])
def load_form_rates():
    return render_template('rates.html')

@app.route('/rates', methods=['GET'])
def get_rates():
    return send_file(LAST_UPLOADED_EXCEL, as_attachment=True)


@app.route('/truck/get', methods=['POST'])
def add_truck():
    if request.method == "POST":
        truck_licence = request.form.get("licence")
        provider_id = request.form.get("provider_id", type=int)
        query1 = "SELECT provider_id from  Providers"
        query2 = "INSERT INTO Trucks (truck_id,provider_id) VALUES ('{}','{}')".format(truck_licence, provider_id)
        try:
            cur = mysql.connection.cursor()
        except:
            return "Faild connection to db,MYSQL_IS_DOWN"
        else:
            cur.execute(query1)
            mysql.connection.commit()
            res = cur.fetchall()
            for var in res:   
                if provider_id == var[0]:
                    cur.execute(query2)
                    mysql.connection.commit()
                    res = cur.fetchall()
            else:
                print (jsonify(res))
                print (res)
            cur.close()
            return jsonify(res)


@app.route('/truck/add', methods=['GET'])
def load_setTruck():
    if request.method == "GET":
        return render_template('setTruck.html')


@app.route('/truck/{id}', methods=['PUT'])
def update_truck():
    return "return render_template('index.html')"

# ===========================================================================


@app.route('/truck/getbyid', methods=['GET'])
def load_get_trucks_form():
    test = get("http://localhost:5000/health")  # weight team API goes here
    print(test)
    return test
    # return render_template('truck7.html')


@app.route('/truck/<id>?from=t1&to=t2', methods=['GET'])
def get_truck():
    return "return render_template('index.html')"


# ===========================================================================


@app.route('/bill/<id>?from=t1&to=t2', methods=['GET'])
def get_bill():
    return "return render_template('index.html')"


@app.route('/health', methods=['GET'])
def get_health():
    query = "SELECT * FROM billdb;"
    try:
        cur = mysql.connection.cursor()
    except:
        return jsonify(cur)
    else:
        # test that the DB is alive by selecting data:
        query = "SELECT * from Providers;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        mysql.connection.commit()
        res = cur.fetchall()
        cur.close()
    return jsonify(res)


# @app.route('/api/healthy', methods=['GET'])
# def get_tasks():
#     return jsonify({'tasks': tasks})


app.run(debug=True, host='0.0.0.0', port=5000)
