#!flask/bin/python

from flask import Flask, jsonify, render_template,request
from flask_mysqldb import MySQL
import csv
import json

from datetime import datetime, date

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

@app.route('/weight', methods=['GET','POST'])
def post_weight():
    if request.method == "POST":
        details = request.form
        direction = details['dir']
        containers = details['containers']
        truck = details['truck']
        weight = details['weight']
        unit = details['unit']
        force = request.form.get('force') #None=false on=true
        produce = details['produce']


        if weight == "":
            return "Error: Weight cant be empty"

        cur = mysql.connection.cursor() #getting last id
        cur.execute(
            "SELECT id FROM sessions ORDER BY id DESC LIMIT 0, 1")
        mysql.connection.commit()
        res = cur.fetchall()

        cur.execute( #getting last direction
            "SELECT direction FROM sessions ORDER BY id DESC LIMIT 0, 1")
        mysql.connection.commit()
        olddir = cur.fetchall()
        olddir = olddir[0][0]

        if res == (): #is the table empty?
            if direction != "in":
                return "ERROR: Empty table, no trucks inbound"
            else:
                res=0
        else:
            res=res[0][0] #its not empty, this is the last id avilable
        
        if direction == "in" or direction == "none":
            if olddir == "in" and force == "None" and direction == "in":
                return "Error: Cant do 'in' after another 'in' without forcing it"
            elif olddir == "in" and force == "on" and direction == "in":
                res-=1 # going to the last id to override it
            elif olddir == "in" and direction == "none":
                return "Error: Cant use 'none' while 'in' is in progress (truck inside doing stuff)"
            
            now = datetime.now() 
            time=now.strftime("%Y%m%d%H%M%S")
            cur.execute("INSERT INTO sessions(direction, date, bruto) VALUES (%s, %s, %s)", (direction, time ,weight))
            mysql.connection.commit()

            if truck == "":
                truck="NA"
            else:
                cur.execute("UPDATE sessions SET trucks_id=%s WHERE id=%s;", (truck, res+1))

            if produce == "":
                produce="NA"
            else:
                cur.execute("UPDATE sessions SET products_id=%s WHERE id=%s;", (produce, res+1))


        elif direction=="out":
            if olddir=="out" and force=="on":
                res-=1 #overriding out
            elif olddir=="out" or olddir=="none":
                return "Error: Cant 'out' without an 'in' (no truck to get out)"
        
        
            cur.execute("UPDATE sessions SET neto=%s WHERE id=%s;", (weight, res+1))

        mysql.connection.commit()
        
        if direction != "out":
            cur.execute("SELECT id, trucks_id, bruto FROM sessions WHERE id=%s;",(res+1,))
            mysql.connection.commit()
            jsoner = cur.fetchall()
            cur.close()
            return jsonify(jsoner)
        else:
            cur.execute(
                "SELECT id, trucks_id, bruto,(bruto-neto) as 'Truck weight', neto FROM sessions WHERE id=%s;", (res+1,))
            mysql.connection.commit()
            jsoner = cur.fetchall()
            cur.close()
            return jsonify(jsoner)

        #whats left is the motherlucking container part 


    return render_template('weight.html')


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
                for line in data: 
                    print(line.values()[0])     #fix this part
                return "this part doesn't work, JSON files SUCK"

        else:
            return "Unsupported file, CSV or JSON files only"

        if error == 0:
            return "New rows added! :)"
        elif error == 1:
            return errmsg
    return render_template('batch.html')


@ app.route('/unknown', methods=['GET'])
def get_unknown():
    try:
        cur = mysql.connection.cursor()
    except:
        return "MYSQL_IS_DOWN"
    else:
        query = "SELECT id FROM containers WHERE weight=0;"
        cur.execute(query)
        mysql.connection.commit()
        res = cur.fetchall()
        cur.close()
        return jsonify(res) 
    

# @ app.route('/weight?from=t1&to=t2&filter=f', methods=['GET'])
# def post_batch_weight():
#     to=request.args.get('to')
#     from1=request.args.get('from')
#     filter1=request.args.get('filter')
#     try:
#         cur = mysql.connection.cursor()
#     except:
#         return "MYSQL_IS_DOWN"
#     else:
#         query = "SELECT id FROM containers WHERE weight=0;"
#         cur.execute(query)
#         mysql.connection.commit()
#         res = cur.fetchall()
#         cur.close()
#         return jsonify(res) 



@app.route('/item/<id>', methods=['GET'])
# /item/<id>?from=t1&to=t2
def get_id(id):
    time=now.strftime("%Y%m")
    test_id=id
    to=request.args.get('to')
    if not to:
        to=now.strftime("%Y%m%d%H%M%S")
    from1=request.args.get('from')

    if not from1:
        from1=time + '01000000'
    # --20181218181512--20181221141414
    try:
        cur = mysql.connection.cursor()
    except:
        return "MYSQL_IS_DOWN"
    else:
        query = ("SELECT trucks_id,bruto,id,date FROM sessions WHERE (trucks_id='{}') and (date BETWEEN '{}' AND '{}');".format(test_id,from1,to))
        cur.execute(query)
        mysql.connection.commit()
        res = cur.fetchall()
        if not res:

            query = ("SELECT sessions.id, containers_has_sessions.containers_id, sessions.date, sessions.bruto FROM containers_has_sessions JOIN sessions ON containers_has_sessions.sessions_id=sessions.id WHERE (containers_has_sessions.containers_id='{}') AND (date BETWEEN '{}' AND '{}');".format(test_id,from1,to))
            cur.execute(query)
            mysql.connection.commit()
            res = cur.fetchall()
            if not res:
                return "not a valid data"
                
        print(res)        
        cur.close()
        return jsonify(res)




@app.route('/item', methods=['GET','POST']) #allow both GET and POST requests
def get_item_id():
    time=now.strftime("%Y%m")
    if request.method == 'POST':  #this block is only entered when the form is submitted
        id=request.form.get('id')
        from1=request.form['from']
        if not from1:
            from1=time + '01000000'       
        to=request.form['to']
        if not to:
            to=now.strftime("%Y%m%d%H%M%S")
        try:
            cur = mysql.connection.cursor()
        except:
            return "MYSQL_IS_DOWN"
        else:
            query = ("SELECT trucks_id,bruto,id,date FROM sessions WHERE (trucks_id='{}') and (date BETWEEN '{}' AND '{}');".format(id,from1,to))
            cur.execute(query)
            mysql.connection.commit()
            res = cur.fetchall()
            if not res:
                query = ("SELECT sessions.id, containers_has_sessions.containers_id, sessions.date, sessions.bruto FROM containers_has_sessions JOIN sessions ON containers_has_sessions.sessions_id=sessions.id WHERE (containers_has_sessions.containers_id='{}') AND (date BETWEEN '{}' AND '{}');".format(test_id,from1,to))
                cur.execute(query)
                mysql.connection.commit()
                res = cur.fetchall()
                if not res:
                    return "not a valid data"
            cur.close()
            return jsonify(res)

    return '''<form method="POST">
                  id: <input type="text" name="id"><br>
                  from: <input type="text" name="from"><br>
                  to: <input type="text" name="to"><br>
                  <input type="submit" value="Submit"><br>
              </form>'''



@ app.route('/session/<id>', methods=['GET'])
def get_session(id):
    test_id=id
    try:
        cur = mysql.connection.cursor()
    except:
        return "MYSQL_IS_DOWN"
    else:
        cur.execute("SELECT direction FROM sessions WHERE (id='{}');".format(test_id))
        mysql.connection.commit()
        inorout = cur.fetchall()
        inorout = inorout[0][0]

        if inorout == "out":
            query = "SELECT sessions.id, sessions.trucks_id, sessions.bruto, sessions.neto, trucks.weight FROM sessions JOIN trucks ON sessions.trucks_id=trucks.truckid WHERE (sessions.id='{}');".format(test_id)
            cur.execute(query)
            mysql.connection.commit()
            res = cur.fetchall()
            cur.close()
            return jsonify(res)
        query = "SELECT id,trucks_id,bruto FROM sessions WHERE (id='{}');".format(test_id)
        cur.execute(query)
        mysql.connection.commit()
        res = cur.fetchall()
        cur.close()
        return jsonify(res) 


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
