#!/usr/bin/env python3
import os , random , shutil , requests , json , pandas as pd
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
from flask import Flask, jsonify , send_file , render_template , request , flash , redirect , url_for
from requests.exceptions import HTTPError


# from config import Config
# from flask_migrate import Migrate
# from flask_sqlalchemy import SQLAlchemy
# connections

# eviroment variables
LAST_UPLOADED_EXCEL = "/tmp/last_excel.xlsx"
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
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

# =================================================================

# Global methods :


def get(url):
    try:
        res = requests.get(url)
        return jsonify(res.json())
    except:
        return "cant connect to the api"

def mysql_execute_query(query):
    try:
        cur = mysql.connection.cursor()
    except:
        flash("Faild connectin,MYSQL_IS_DOWN")
    else:
        cur.execute(query)
        mysql.connection.commit()
        res = cur.fetchall()
        cur.close()
        return res
def timeformat(data):
    return (data[0:4]+data[5:7]+data[8:10]+data[11:13]+data[14:16]+"00")

# ====================================================================


# Routing:

@app.route('/')
def home():
    return render_template("main.html")

@app.route('/provider/reg', methods=['POST'])
def get_tasks():
    providerName = request.form.get("p_name")
    query ="SELECT provider_name from Providers"
    res = mysql_execute_query(query)
    for var in res:   
        if providerName == var[0]:
            flash("Provider name allready exsits", "info")
            return render_template('index.html')     
    
    query = "INSERT INTO Provider (name) VALUES ('{}')".format(providerName)
    mysql_execute_query(query)
    query = "SELECT * FROM Provider WHERE name=('{}')".format(providerName)
    res = mysql_execute_query(query)
    return jsonify(res)

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
    base_name_to_use = "flask_tmp_file_" + \
        str(random.randint(10000000000, 99999999999)) + \
        "_" + secure_filename(base_name_to_use)
    return os.path.join("/tmp", base_name_to_use)

@app.route('/rates/reg', methods=['POST'])
def upload_rates():
    files_to_delete_when_function_finishes = []
    try:
        f = request.files['file']
        # checkfile
        if (not allowed_file(f.filename)):
            return "not an excel file : try again"

        # save excel file to disk
        excel_file_temp_path = get_safe_temp_filename(f.filename)
        f.save(excel_file_temp_path)
        files_to_delete_when_function_finishes.append(excel_file_temp_path)

        # convert to csv
        csv_file_temp_path = get_safe_temp_filename("newfile.csv")
        excel_to_csv = pd.read_excel(excel_file_temp_path)
        excel_to_csv.to_csv(csv_file_temp_path, index=None, header=True)
        files_to_delete_when_function_finishes.append(csv_file_temp_path)

        # insetr into database
        query = "DELETE FROM Products "
        mysql_execute_query(query)

        query = """LOAD DATA LOCAL INFILE '{}' INTO TABLE Products FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS """
        query = query.format(csv_file_temp_path)
        mysql_execute_query(query)

        query = "SELECT * FROM Products "
        cur = mysql.connection.cursor()
        cur.execute(query)
        res = cur.fetchall()
        cur.close()

        # save last file
        if os.path.isfile(LAST_UPLOADED_EXCEL):
            os.remove(LAST_UPLOADED_EXCEL)
        shutil.copy(excel_file_temp_path, LAST_UPLOADED_EXCEL)
        return jsonify(res)

    # except:
    #     return 'Somthing went wrong, try again :)'

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
        if not request.form["licence"]:
            flash("licence is required", "info")
            return render_template('setTruck.html')
        elif not request.form["provider_id"]:
            flash("provider_id is required", "info")
            return render_template('setTruck.html')
        else:
            truck_licence = request.form.get("licence")
            provider_id = request.form.get("provider_id", type=int)
            query = "SELECT truck_id from Trucks"
            res = mysql_execute_query(query)
            for var in res:
                if truck_licence == var[0]:
                    flash("licence is alredy exsits!")
                    return render_template('setTruck.html') 

            query = "SELECT provider_id from Providers"
            res = mysql_execute_query(query)
            for var in res:
                if provider_id == var[0]:
                    query = "INSERT INTO Trucks (truck_id,provider_id) VALUES ('{}','{}')".format(
                        truck_licence, provider_id)
                    mysql_execute_query(query)
                    break
            else:
                flash("Provider id not exsits!")
                return render_template('setTruck.html')

    return redirect(url_for("home"))


@app.route('/truck/add', methods=['GET'])
def load_setTruck():
    if request.method == "GET":
        return render_template('setTruck.html')


@app.route('/truck/{id}', methods=['PUT'])
def update_truck():
    if request.method == "PUT":
        return "return render_template('index.html')"


@app.route('/truck/insert', methods=['GET'])
def load_detalis_for_truck():
    if request.method == "GET":
        return render_template('truck_details.html')

@app.route('/truck/getbyid', methods=['POST','GET'])
def load_get_trucks_form(id=-1,fro='',to=''):
    if not request.form["licence"]:
        flash("truck_id is required", "error")
        return render_template('truck_details.html')
    elif not request.form["t1"] or not request.form["t2"] :
        flash("Please insert time", "info")
        return render_template('truck_details.html')
    else:
        flag=0
        if id == -1:
            flag=1
            id = request.form.get("licence")
        query ="SELECT '{}' from Trucks".format(id)
        res = mysql_execute_query(query)
        for var in res:
            if id == var[0]:
                par = {} 
                if fro == '':
                    fro = request.form.get("t1")
                if to == '':
                    to = request.form.get("t2")
                fro=timeformat(fro)
                to=timeformat(to)
                par = {"id":f'{id}',"from":f'{fro}',"to":f'{to}'}
                try:
                    response = requests.post("http://blue.develeap.com:8089/item", data = par)
                    if flag == 1:
                        return jsonify(response.text)
                    return response.text

                except HTTPError as http_err:
                    print(f'HTTP error occurred: {http_err}')
                except Exception as err:
                    print(f'Other error occurred: {err}')
                break
            print(var[0])
        else:
            flash("truck id not found,please insert agein", "info")
            return render_template('truck_details.html')
    
@app.route('/bill/insert', methods=['GET'])
def load_detalis_for_bill():
    if request.method == "GET":
        return render_template('truck_details.html')

@app.route('/bill/getbyid', methods=['POST'])
def get_bill():
    id = request.form.get("licence")
    fro = request.form.get("t1")
    to = request.form.get("t2")
    res1 = load_get_trucks_form(id,timeformat(fro),timeformat(to))
    query = "SELECT Trucks.provider_id,Providers.provider_name,Providers.payment_timing from Trucks join Providers on Trucks.provider_id=Providers.provider_id where Trucks.truck_id={}".format(id)
    res2 = mysql_execute_query(query)
    jsonbill = [{"provider id":f'{res2[0][0]}',"name": f'{res2[0][1]}',"from": f'{fro}',"to": f'{to}',"licence": f'{id}',}]
    num=''
    total=0
    list_res=[]
    for var in res1.split(':')[-1]:
        if var.isdigit():
            num+=var
        else:
            response = requests.post("http://blue.develeap.com:8089/session", data={"id":f'{num}'})
            sess = (response.text)
            sess=sess.split(',')
            if sess[0] == "Error: No such session ID exist":
                continue
            num_session=''
            for session in sess[-1]:
                if var.isdigit():
                    num_session+=session
                else:
                    query = "SELECT distinct rate,product_name from Products where product_id=3"
                    # .format(id)
                    res3 = mysql_execute_query(query)
                    num_session=''
                    sss=res3[0][1]
                    print(res3)
                    print(res3[0][1])
                    pok=sss
                    print(pok)
                    print("-------------------------------------------------")
                    hhh=sess[2].split(":")[-1]
                    pok2=hhh[0:-3]
                    print(pok,pok2)
                    pay=int(pok)*int(pok2)
                    prod=[{"sessionCount":f'{sess[0].split(":")[-1]}'},{ "product":f'{res3[0][0]}',"amount": f'{sess[2].split(":")[-1]}', "rate": f'{res3[0][1]}', "pay": f'{pay}'}]
                    list_res+=prod
                    total+=pay
                    break
       
    return jsonify(jsonbill,list_res,{"total":f'{total}'})

@app.route('/health', methods=['GET'])
def get_health():
    query = "SELECT truck_id from Trucks;"
    res = mysql_execute_query(query)
    return jsonify(res)


app.run(debug=True, host='0.0.0.0', port=5000)
