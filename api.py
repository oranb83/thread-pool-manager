import os

from flask import Flask, abort, request, jsonify
from flask_expects_json import expects_json

from orchestrator import Orchestrator

CONTENT_TYPE_TEXT = 'application/json'
DEBUG = os.getenv('DEBUG', False)
app = Flask(__name__)
schema = {
    'type': 'object',
    'properties': {
        'type': {'type': 'string'},
        'task': {'type': 'string'},
        'parameters': {'type': 'array'}
    },
    'required': ['type', 'task']
}

orchest = Orchestrator()


@app.route('/health')
def health():
    return 'Strong like a bull!'


@app.route('/task', methods=['POST'])
@expects_json(schema)
def post_message():
    payload = request.json
    pool = orchest.get_or_create_pool(payload['type'])
    try:
        orchest.add_task(pool, eval(payload['task']), *payload['parameters'])
    except Exception as e:
        return 'task failed: {}'.format(str(e)), 500

    return 'created', 201


@app.route('/task/<pool_type>', methods=['GET'])
def get_message(pool_type):
    if not pool_type:
        abort(400)

    pool = orchest.get_or_create_pool(pool_type)
    try:
        results = orchest.get_results(pool)
    except Exception as e:
        return 'task failed: {}'.format(str(e)), 500

    return jsonify(results)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=DEBUG, threaded=True)
