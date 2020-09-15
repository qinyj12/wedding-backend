from flask import Blueprint, current_app, make_response
from flask_restful import Api, Resource, reqparse
import requests, time, hashlib
import random

# 自定义一个生成随机字符串的类
class Random_str():
    def __init__(self, count):
        self.count = count
        self.mother_list = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'
    def __repr__(self):
        return ''.join([random.choice(self.mother_list) for _ in range(self.count)])

app = Blueprint('wx_api', __name__, url_prefix = '/wx')
api = Api(app)
parser = reqparse.RequestParser()

class Wx_api(Resource):
    def get(self):
        return make_response('hello wx')

class Access_permission(Resource):
    def get(self):
        # 生成token
        access_token = requests.get(
            url = 'https://api.weixin.qq.com/cgi-bin/token?', 
            params = {
                "grant_type": 'client_credential',
                'appid':'wxe0e65e72672a7c5d',
                'secret':'20d9cf9334f1750b8df6655e5fbb09aa',
            }
        ).json()['access_token']

        # 生成ticket
        ticket = requests.get(
            url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket',
            params = {
                'access_token': access_token,
                'type': 'jsapi'
            }
        ).json()['ticket']

        # 随机字符串，使用我自定义的类
        noncestr = str(Random_str(16))
        # 时间戳
        timestamp = round(time.time())
        # 请求地址，就是前端的地址
        parser.add_argument('url', type = str, location = 'args')
        args = parser.parse_args()
        request_url = args['url']

        # 组合成一个新字符串
        temp_str = 'jsapi_ticket=' + ticket + '&noncestr=' + noncestr + '&timestamp=' + str(timestamp) + '&url=' + request_url

        # 再把这个新字符串用sha1加密，这样就形成了签名
        signature = hashlib.sha1(temp_str.encode('utf-8')).hexdigest()

        # 返回
        return {'nonceStr': noncestr, 'timestamp': timestamp, 'signature': signature}

class Weixin_page(Resource):
    def get(self):
        return current_app.send_static_file('index.html')


api.add_resource(Wx_api, '/')
api.add_resource(Access_permission, '/access')
api.add_resource(Weixin_page, '/page')