import math
import time
from flask import Flask, jsonify, make_response, abort, request

app = Flask(__name__)

VERSION = '0.1'

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

# dummy API
@app.route('/api/v{}/theanswer'.format(VERSION), methods=['GET'])
def theanswer():
    return jsonify({ 'answer': 42 })

# add API
@app.route('/api/v{}/add'.format(VERSION), methods=['POST'])
def add():
    if not request.json or not 'data' in request.json:
        abort(400)

    jsonraw = request.json
    result = -1.0
    if 'data' in jsonraw and len(jsonraw['data']) > 0:
        result = sum(jsonraw['data'])

    return jsonify({ 'result': result })

# silly work API
@app.route('/api/v{}/dowork'.format(VERSION), methods=['POST'])
def dowork():
    if not request.json or not 'data' in request.json:
        abort(400)

    jsonraw = request.json
    result = -1.0
    if 'data' in jsonraw and len(jsonraw['data']) > 0:
        result = 2.4
        for d in jsonraw['data']:
            result += math.pow(float(d)*4.51e2/5.123e2, 2.3)

    time.sleep(3)
    return jsonify({ 'result': result })

@app.route('/')
def index():
    return "Test rest API v{0}".format(VERSION)

if __name__ == '__main__':
    app.run(
        debug=False,
        host='0.0.0.0',
        port=8080
    )
