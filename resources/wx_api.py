from flask import Blueprint, current_app, make_response, redirect, url_for, request
from flask_restful import Api, Resource, reqparse
from .cache import cache
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

# 单纯用来测试路由的
class Wx_api(Resource):
    def get(self):
        return request.url_root.replace(request.script_root, '')

# 定义一个获取token和ticket的资源
class Token_and_ticket(Resource):
    # token和ticket有7200秒有效期，这里缓存7000秒
    @cache.cached(timeout = 7000)
    def get(self):
        # 请求token接口
        request_token = requests.get(
            url = 'https://api.weixin.qq.com/cgi-bin/token?', 
            params = {
                "grant_type": 'client_credential',
                # 公众号飞快的香港记者的appid和secret
                # 'appid':'wx5654d7882a1bdf03',
                # 'secret':'13ab13979d6a36a518f19bd2f4c4b664',
                # 测试号的appid和secret
                'appid':'wxe0e65e72672a7c5d',
                'secret':'20d9cf9334f1750b8df6655e5fbb09aa',
            }
        ).json()

        # 先把返回值打印出来看看有没有问题
        # import sys
        # print(request_token, file=sys.stderr)

        # 然后生成token
        access_token = request_token['access_token']

        # 生成ticket
        ticket = requests.get(
            url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket',
            params = {
                'access_token': access_token,
                'type': 'jsapi'
            }
        ).json()['ticket']

        # 因为只是后端调用这个接口，所以不要json格式
        return make_response({'token': access_token, 'ticket': ticket})

# 定义一个获取签名的资源
class Signature(Resource):
    def get(self):
        # 先获取当前域名，切换测试、服务器地址比较麻烦，动态获取更好
        current_hostname = request.url_root.replace(request.script_root, '')
        # 调用自己的接口，获取token和ticket
        token_and_ticket = requests.get(current_hostname + url_for('wx_api.token_and_ticket')).json()

        import sys
        print(token_and_ticket,file=sys.stderr)

        token, ticket = token_and_ticket['token'], token_and_ticket['ticket']

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
        return {'nonceStr': noncestr, 'timestamp': timestamp, 'signature': signature, 'ticket': ticket, 'url': request_url, 'string1': temp_str}

class Weixin_page(Resource):
    def get(self):
        return current_app.send_static_file('index.html')


api.add_resource(Wx_api, '/')
# api.add_resource(Access_permission, '/access')
api.add_resource(Weixin_page, '/page')
api.add_resource(Token_and_ticket, '/tokenandticket')
api.add_resource(Signature, '/signature')