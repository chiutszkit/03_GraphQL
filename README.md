<h1>HW_03 GrqphQL

<h3>This is a Python Project to server API Requests</h3>

## How To Use Python

### Create Environment (For First Time)

```
python3 -m venv .venv
```

### Setup Proxy
```
pip config set global.proxy http://proxy.my-proxy-domain.com:my-proxy-port
pip config set global.trusted-host pypi.python.org\npypi.org\nfiles.pythonhosted.org
```

### Create or Update requirements.txt
```
pip freeze > requirements.txt
```

## Run 

### Run Virtual Environment
```
source .venv/bin/activate
```

### Install dependencies
```
pip install -r requirements.txt
```

### Run the App
```
python3 api_server.py
```
The Flask App is configured for you. Running it on http://127.0.0.1:5000

## Sample Requests

Type the command(s) in another Terminal when Running the App

### Create a new todo:
```
curl -X POST http://localhost:5000/todos -H "Content-Type: application/json" -d '{"title": "Learn Flask", "description": "Study Flask documentation"}'
```

### Get all todos:
```
curl http://localhost:5000/todos
```

### Update a todo:
```
curl -X PUT http://localhost:5000/todos/1 -H "Content-Type: application/json" -d '{"completed": true}'
```

### Delete a todo:
```
curl -X DELETE http://localhost:5000/todos/1
```