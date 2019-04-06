import os

from flask import Flask, abort, request, jsonify
from flask_expects_json import expects_json

from orchestrator import Orchestrator

CONTENT_TYPE_TEXT = 'application/json'
DEBUG = os.getenv('DEBUG', True)
app = Flask(__name__)
schema = {
    'type': 'object',
    'properties': {
        'type': {'type': 'string'},
        'task': {'type': 'string'}
    },
    'required': ['type', 'task']
}

orchest = Orchestrator()

@app.route('/health')
def health():
    return 'Strong like a bull!'


@app.route('/worker', methods=['POST'])
@expects_json(schema)
def post_message():
    payload = request.json
    schema_properties = schema['properties'].keys()
    if len(payload) > len(schema_properties):
        return 'bad request, only {} are allowed in the payload'.format(schema_properties), 400

    pool = orchest.get_or_create_pool(payload['type'])
    try:
        pool.run(task)
    except Exception as e:
        return 'task failed: {}'.format(str(e)), 500

    return 'created', 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=DEBUG, threaded=True)
