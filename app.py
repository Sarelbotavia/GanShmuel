#!flask/bin/python
from flask import Flask, jsonify
from flask import render_template
app = Flask(__name__)


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/provider', methods=['POST'])
def add_provider():
    return "return render_template('index.html')"

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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port="5000")
