from flask import Flask, request

from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from

app = Flask(__name__)

app.json_encoder = LazyJSONEncoder

swagger_template = dict(
info = {
    'title': LazyString(lambda: 'My first Swagger UI document'),
    'version': LazyString(lambda: '0.1'),
    'description': LazyString(lambda: 'This document depicts a      sample Swagger UI document and implements Hello World functionality after executing GET.'),
    },
    host = LazyString(lambda: request.host)
)

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'hello_world',
            "route": '/hello_world.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

@swag_from("hello_world.yml", methods=['GET'])
@app.route('/')
def hello_world():
    return 'hello world!'

swagger = Swagger(app, template=swagger_template,             
                config=swagger_config)


@swag_from("username.yml", methods = ["GET"])
@app.route('/<name>')
def another_response(name):
    return f'You entered the name {name}'


@swag_from("login.yml", methods=["GET", "POST"])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return {
            'name': 'Alfonso',
            'age': 23
        }
    else:
        return 'Has usado otro metodo. Usa POST'


'''
El JSON que debe recibir el siguiente endpoint debe ser de la forma:
{
    "name": string,
    "last_name": string
}
'''


@app.route('/query', methods = ["POST"])
def database_query():
    if request.method == 'POST':
        name = request.form.get("name")
        last_name = request.form.get("last_name")
        return f'El nombre es {name} y el apellido es {last_name}'


if __name__ == '__main__':
    app.run()