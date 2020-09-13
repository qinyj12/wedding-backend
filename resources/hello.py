from flask import Blueprint
from flask_restful import Api, Resource

app = Blueprint('hello', __name__, url_prefix = '/hello')

api = Api(app)

class Hello(Resource):
    def get(self):
        return {'result': 'hello world'}

api.add_resource(Hello, '/')