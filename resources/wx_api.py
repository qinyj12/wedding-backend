from flask import Blueprint, current_app, request
from flask_restful import Api, Resource
import requests, time, hashlib

from requests.models import codes

app = Blueprint('wx_api', __name__, url_prefix = '/wx')

api = Api(app)

class Wx_api(Resource):
    def get(self):
        return request.url

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

        # 随机字符串
        noncestr = 'Wm3WZYTPz0wzccnW'
        # 时间戳
        timestamp = round(time.time())
        # 请求地址
        request_url = request.url

        # 组合成一个新字符串
        temp_str = 'jsapi_ticket=' + ticket + '&noncestr=' + noncestr + '&timestamp=' + str(timestamp) + '&url=' + request_url

        # sha1加密
        sha1 = hashlib.sha1()
        sha1.update(temp_str.encode('utf-8'))

        # 生存signature
        signature = sha1.hexdigest().upper()

        import sys
        print({'noncestr': noncestr, 'timestamp': timestamp, 'signature': signature, 'url': request_url}, file = sys.stderr)
        # 返回
        return {'noncestr': noncestr, 'timestamp': timestamp, 'signature': signature}

class Weixin_page(Resource):
    def get(self):
        return current_app.send_static_file('index.html')


api.add_resource(Wx_api, '/')
api.add_resource(Access_permission, '/access')
api.add_resource(Weixin_page, '/page')