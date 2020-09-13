from flask import Blueprint, current_app
from flask_restful import Api, Resource

app = Blueprint('wx_callback', __name__)

api = Api(app)

class MP_verify(Resource):
    def get(self):
        return current_app.send_static_file('MP_verify_ErVytttLPsIDzh7X.txt')

api.add_resource(MP_verify, '/MP_verify_ErVytttLPsIDzh7X.txt')