#!flask/bin/python

from flask import Flask, jsonify, render_template, request
from flask_mysqldb import MySQL
import csv
import json
import numpy as np   # <<< wtf is this

from datetime import datetime, date

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_HOST'] = 'Blue.develeap.com'
#app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'weight'
app.config['MYSQL_PASSWORD'] = '123'
app.config['MYSQL_DB'] = 'weight_db'
app.config['MYSQL_PORT'] = 8086

mysql = MySQL(app)
now = datetime.now()


def func(arr, arg):
    list_1 = []

    for i in range(arr.shape[0]):
        j = 0
        for a in arg.split(','):
            list_1.append((a + ':'+str(arr[int(i)][int(j)])))
            j += 1

    return list_1


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/weight', methods=['GET', 'POST'])
def post_weight():
    if request.method == "POST":
        details = request.form
        direction = details['dir']
        containers = details['containers']
        truck = details['truck']
        weight = details['weight']
        unit = details['unit']
        force = request.form.get('force')  # None=false on=true
        produce = details['produce']

        if weight == "":
            return "Error: Weight cant be empty"

        cur = mysql.connection.cursor()  # getting last id
        cur.execute(
            "SELECT id FROM sessions ORDER BY id DESC LIMIT 0, 1")
        mysql.connection.commit()
        res = cur.fetchall()

        cur.execute(  # getting last direction
            "SELECT direction FROM sessions ORDER BY id DESC LIMIT 0, 1")
        mysql.connection.commit()
        olddir = cur.fetchall()
        olddir = olddir[0][0]

        if res == ():  # is the table empty?
            if direction != "in":
                return "ERROR: Empty table, no trucks inbound"
            else:
                res = 0
        else:
            res = res[0][0]  # its not empty, this is the last id avilable

        if direction == "in" or direction == "none":
            if olddir == "in" and direction == "in":
                if force != "on":
                    return "Error: Cant do 'in' after another 'in' without forcing it"
                else:
                    res = res-1  # going to the last id to override it
            elif olddir == "in" and direction == "none":
                return "Error: Cant use 'none' while 'in' is in progress (truck inside doing stuff)"

            now = datetime.now()
            time = now.strftime("%Y%m%d%H%M%S")
            if olddir != "in" and (direction == "in" or direction == "none"):
                cur.execute(
                    "INSERT INTO sessions(direction, date, bruto) VALUES (%s, %s, %s)", (direction, time, weight))
            else:
                cur.execute("UPDATE sessions SET direction=%s, date=%s, bruto=%s where id=%s", (
                    direction, time, weight, res+1))  # force already checked before so no need to double check
            mysql.connection.commit()

            if truck == "":
                truck = "NA"
            else:
                cur.execute(
                    "UPDATE sessions SET trucks_id=%s WHERE id=%s;", (truck, res+1))

            if produce == "":
                produce = "NA"
            else:
                cur.execute(
                    "UPDATE sessions SET products_id=%s WHERE id=%s;", (produce, res+1))

        elif direction == "out":
            if olddir == "none" or (force != "on" and olddir == "out"):
                return "Error: Cant 'out' without an 'in' (no truck to get out, you can force it if its 'out')"

            cur.execute(
                "UPDATE sessions SET neto=%s, direction=%s WHERE id=%s;", (weight, direction, res))

        if direction == 'in' and containers != "":
            if force == "on":
                cur.execute(
                    "DELETE FROM containers_has_sessions WHERE sessions_id=%s;", (res+1,))

            errorcont = 0
            errmsgcont = "Action completed, BUT the following containers could not be added because they do not exist in database! Please add the missing containers and override by using force ('in' only!):\n"

            for word in containers.split(','):
                try:
                    cur.execute(
                        "INSERT INTO containers_has_sessions(containers_id, sessions_id) VALUES (%s, %s)", (word, res+1))
                except:
                    errorcont = 1
                    errmsgcont += word+"\n"
            mysql.connection.commit()

            if errorcont == 1:
                cur.close()
                return errmsgcont

        if direction != "out":
            cur.execute(
                "SELECT id, trucks_id, bruto FROM sessions WHERE id=%s;", (res+1,))
            mysql.connection.commit()
            jsoner = cur.fetchall()
            cur.close()
            jsoner = np.array(jsoner)
            return jsonify(func(jsoner, "id,trucks_id,bruto"))
        else:
            cur.execute(
                "SELECT id, trucks_id, bruto,(bruto-neto) as 'Truck weight', neto FROM sessions WHERE id=%s;", (res,))
            mysql.connection.commit()
            jsoner = cur.fetchall()
            cur.close()
            jsoner = np.array(jsoner)
            return jsonify(func(jsoner, "id,trucks_id,bruto,Truck_weight,neto"))

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

        elif listfile.endswith('.json'):        # key[0]=unit
            with open('in/' + listfile) as f:   # key[1]=id
                data = json.load(f)             # key[2]=weight

            cur = mysql.connection.cursor()
            for line in data:
                try:
                    cur.execute(
                        "INSERT INTO containers(id, weight, unit) VALUES (%s, %s, %s)", (line.values()[1], line.values()[2], line.values()[0]))
                except:
                    error = 1
                    errmsg += str(line.values()[1])+", " + \
                        str(line.values()[2])+", "+line.values()[0]+"\n"

            mysql.connection.commit()
            cur.close()

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
        m = np.array(res)
        return jsonify(func(m, 'id'))


@ app.route('/getweight', methods=['GET'])
# /getweight?from=t1&to=t2&filter=f
def get_weight():

    to = request.args.get('to')
    from1 = request.args.get('from')
    filter1 = request.args.get('filter')
    now = datetime.now()

    if not from1:
        from1 = now.strftime("%Y%m%d")+"000000"
    if not to:
        now = datetime.now()
        to = now.strftime("%Y%m%d%H%M%S")
    if not filter1:
        filter1 = "in,out,none"

    finalres = ()
    try:
        cur = mysql.connection.cursor()
    except:
        return "MYSQL_IS_DOWN"
    else:
        for direction in filter1.split(','):

            session = (
                "SELECT sessions.id FROM sessions WHERE (sessions.direction='{}');".format(direction))
            cur.execute(session)
            mysql.connection.commit()
            session = cur.fetchall()

            for s in session:
                res = ()
                query = ("SELECT Distinct sessions.id, sessions.direction, sessions.bruto, sessions.neto, sessions.products_id, GROUP_CONCAT(containers_has_sessions.id) FROM containers_has_sessions JOIN sessions ON containers_has_sessions.sessions_id=sessions.id WHERE (sessions.direction='{}') AND (sessions.id='{}') AND (date BETWEEN '{}' AND '{}');".format(
                    direction, s[0], from1, to))
                cur.execute(query)
                mysql.connection.commit()
                res += cur.fetchall()
                finalres += (res[0],)

    cur.close()
    return jsonify(finalres)


@app.route('/item/<id>', methods=['GET'])
# /item/<id>?from=t1&to=t2
def get_id(id):
    time = now.strftime("%Y%m")
    test_id = id
    to = request.args.get('to')
    if not to:
        to = now.strftime("%Y%m%d%H%M%S")
    from1 = request.args.get('from')

    if not from1:
        from1 = time + '01000000'
    # --20181218181512--20181221141414
    try:
        cur = mysql.connection.cursor()
    except:
        return "MYSQL_IS_DOWN"
    else:
        query = ("SELECT DISTINCT trucks_id,bruto,GROUP_CONCAT(id) FROM sessions WHERE (trucks_id='{}') and (date BETWEEN '{}' AND '{}');".format(
            test_id, from1, to))
        cur.execute(query)
        mysql.connection.commit()
        res = cur.fetchall()
        if not res:

            query = ("SELECT DISTINCT containers_has_sessions.containers_id, sessions.bruto, GROUP_CONCAT(sessions.id) FROM containers_has_sessions JOIN sessions ON containers_has_sessions.sessions_id=sessions.id WHERE (containers_has_sessions.containers_id='{}') AND (date BETWEEN '{}' AND '{}');".format(test_id, from1, to))
            cur.execute(query)
            mysql.connection.commit()
            res = cur.fetchall()
            cur.close()
            m = np.array(res)
            return jsonify(func(m, 'containers id,bruto,sessions'))
            if not res:
                return "not a valid data"

        cur.close()
        m = np.array(res)
        return jsonify(func(m, 'session id,trucks id,bruto,sessions'))


# allow both GET and POST requests
@app.route('/item', methods=['GET', 'POST'])
def get_item_id():
    time = now.strftime("%Y%m")
    if request.method == 'POST':  # this block is only entered when the form is submitted
        test_id = request.form.get('id')
        from1 = request.form['from']
        if not from1:
            from1 = time + '01000000'
        to = request.form['to']
        if not to:
            to = now.strftime("%Y%m%d%H%M%S")
        try:
            cur = mysql.connection.cursor()
        except:
            return "MYSQL_IS_DOWN"
        else:
            query = ("SELECT DISTINCT sessions.trucks_id, GROUP_CONCAT(DISTINCT bruto-neto), GROUP_CONCAT(sessions.id) FROM sessions WHERE (sessions.trucks_id='{}') and (date BETWEEN '{}' AND '{}');".format(test_id, from1, to))
            cur.execute(query)
            mysql.connection.commit()
            res = cur.fetchall()
            if res[0][0] == None:
                print("haymon limon!!")
                query = ("SELECT DISTINCT containers_has_sessions.containers_id, GROUP_CONCAT(DISTINCT (sessions.bruto-sessions.neto)), GROUP_CONCAT(sessions.id) FROM containers_has_sessions JOIN sessions ON containers_has_sessions.sessions_id=sessions.id WHERE (containers_has_sessions.containers_id='{}') AND (date BETWEEN '{}' AND '{}');".format(test_id, from1, to))
                cur.execute(query)
                mysql.connection.commit()
                res = cur.fetchall()
                cur.close()
                m = np.array(res)
                if res[0][0] == None:
                    return "not a valid data"
                return jsonify(func(m, 'containers id,tara,sessions'))
            cur.close()
            m = np.array(res)
            return jsonify(func(m, 'trucks id,tara,sessions'))
            # return jsonify(res)

    return render_template('item.html')


@ app.route('/session', methods=['GET', 'POST'])
def get_session_UI():
    if request.method == 'POST':
        test_id = request.form.get('id')
        try:
            cur = mysql.connection.cursor()
        except:
            return "MYSQL_IS_DOWN"
        else:
            cur.execute(
                "SELECT direction FROM sessions WHERE (id='{}');".format(test_id))
            mysql.connection.commit()
            inorout = cur.fetchall()
            if inorout != ():
                inorout = inorout[0][0]
            else:
                return "Error: No such session ID exist"

            if inorout == "out":
                query = "SELECT sessions.id, trucks_id, bruto, neto, bruto-neto, products_id FROM sessions WHERE (sessions.id='{}');".format(
                    test_id)
                cur.execute(query)
                mysql.connection.commit()
                res = cur.fetchall()
                cur.close()
                m = np.array(res)
                return jsonify(func(m, 'id,trucks id,bruto,neto,truck weight,products id'))
            query = "SELECT id,trucks_id,bruto,products_id FROM sessions WHERE (id='{}');".format(
                test_id)
            cur.execute(query)
            mysql.connection.commit()
            res = cur.fetchall()
            cur.close()

            m = np.array(res)
            return jsonify(func(m, 'id,trucks id,bruto,products id'))
    return render_template('sessions.html')


@ app.route('/session/<id>', methods=['GET'])
def get_session(id):
    test_id = id
    try:
        cur = mysql.connection.cursor()
    except:
        return "MYSQL_IS_DOWN"
    else:
        cur.execute(
            "SELECT direction FROM sessions WHERE (id='{}');".format(test_id))
        mysql.connection.commit()
        inorout = cur.fetchall()
        inorout = inorout[0][0]

        if inorout == "out":
            query = "SELECT sessions.id, sessions.trucks_id, sessions.bruto, sessions.neto, bruto-neto FROM sessions WHERE (sessions.id='{}');".format(
                test_id)
            cur.execute(query)
            mysql.connection.commit()
            res = cur.fetchall()
            cur.close()
            m = np.array(res)
            return jsonify(func(m, 'id,trucks id,bruto,neto,truck weight'))
        query = "SELECT id,trucks_id,bruto FROM sessions WHERE (id='{}');".format(
            test_id)
        cur.execute(query)
        mysql.connection.commit()
        res = cur.fetchall()
        cur.close()

        m = np.array(res)
        return jsonify(func(m, 'id,trucks id,bruto'))


@ app.route('/health', methods=['GET'])
def get_health():
    try:
        cur = mysql.connection.cursor()
    except:
        return "MYSQL_IS_DOWN"
    else:
        cur.close()
        return jsonify(("RUNNING",))


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
