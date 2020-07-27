#!flask/bin/python
from flask import Flask, jsonify

app = Flask(_name_)


@app.route('/')
def index():
    return "Hello, World!"

@app.route('/provider', methods=['POST'])
def post_provider():
    return "provider"
    #init unique id

@app.route('/rates', methods=['POST'])
def post_rates():
    return "rates"

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
    return "health"


#@app.route('/api/healthy', methods=['GET'])
# def get_tasks():
#     return jsonify({'tasks': tasks})


if _name_ == '_main_':
    app.run(debug=True)
    