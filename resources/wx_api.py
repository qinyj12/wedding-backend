from flask import Blueprint, current_app
from flask_restful import Api, Resource
import requests

app = Blueprint('wx_api', __name__, url_prefix = '/wx')

api = Api(app)

class Wx_api(Resource):
    def get(self):
        return {'result': 'hello wx'}

class Access_token(Resource):
    def get(self):
        Access_token = requests.get(
            url = 'https://api.weixin.qq.com/cgi-bin/token?', 
            params = {
                "grant_type": 'client_credential',
                'appid':'wxe0e65e72672a7c5d',
                'secret':'20d9cf9334f1750b8df6655e5fbb09aa',
            }
        ).json()
        return Access_token

class Weixin_page(Resource):
    def get(self):
        return current_app.send_static_file('index.html')


api.add_resource(Wx_api, '/')
api.add_resource(Access_token, '/accesstoken')
api.add_resource(Weixin_page, '/page')