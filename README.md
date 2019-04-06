# Thread Pool Manager
## Description
This is an implementation of thread pool manager in Python3.

## Installation
1. Install python3 latest version (tested on python 3.7.2)
1. Create a virtual environment: `virtualenv --python $(which python3) ~/Envs/manager_venv`
1. Activate virtual environment: `source ~/Envs/manager_venv/bin/activate`
1. Run dependencies: `pip install -r requirements.txt`

## Start server
1. Make sure you've activated the virtual environment as described above in installation *step #3*.
1. Run: `python api.py`

## API
1. Add new tasks: `curl -X POST http://localhost:5000/task -H 'content-type: application/json' -d '{"type": "int", "task": "lambda x, y : x + y", "parameters": [3,4]}'`
1. Get pool results: `curl http://localhost:5000/task/<pool_type>`

## Example of the API test run that I've made
`curl -X POST http://localhost:5000/task -H 'content-type: application/json' -d '{"type": "int", "task": "lambda x, y : x + y", "parameters": [3,4]}'`

`curl -X POST http://localhost:5000/task -H 'content-type: application/json' -d '{"type": "int", "task": "lambda x, y : x + y", "parameters": [1,4]}'`

`curl -X POST http://localhost:5000/task -H 'content-type: application/json' -d '{"type": "int2", "task": "lambda x, y : x + y", "parameters": [2,4]}'`

`curl -X POST http://localhost:5000/task -H 'content-type: application/json' -d '{"type": "int2", "task": "lambda x, y : x + y", "parameters": [2,3]}'`

`curl http://localhost:5000/task/int2` => [6,5]

`curl http://localhost:5000/task/int` => [7,5]

## Test
Run: `python example.py`

**Note:**
I did not add unit-tests nor integration tests, since it's time consuming and this code is not meant to be deployed to production as is.
Having said that you can find an example script that runs tests with debug logs to demonstrate a working flow with all major cases.

There are two tests:
1. `test_pool`
1. `test_orchestrator`
