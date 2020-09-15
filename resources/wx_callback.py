from flask import Blueprint, current_app, make_response
from flask_restful import Api, Resource, reqparse
import hashlib

app = Blueprint('wx_callback', __name__)
api = Api(app)
parser = reqparse.RequestParser()

# 用于JS接口安全域名
class MP_verify(Resource):
    def get(self):
        return current_app.send_static_file('MP_verify_ErVytttLPsIDzh7X.txt')

# 用于基本配置->token
class Token_verify(Resource):
    def get(self):
        parser.add_argument('signature', type = str, location = 'args')
        parser.add_argument('timestamp', type = str, location = 'args')
        parser.add_argument('nonce', type = str, location = 'args')
        parser.add_argument('echostr', type = str, location = 'args')
        args = parser.parse_args()

        signature = args['signature']
        timestamp = args['timestamp']
        nonce  = args['nonce']
        echostr = args['echostr']
        token = '57fzrg'

        import sys
        print(signature, file = sys.stderr)
        print(timestamp, file = sys.stderr)
        print(nonce, file = sys.stderr)
        print(echostr, file = sys.stderr)
        print(token, file = sys.stderr)

        list = [token, timestamp, nonce]
        list.sort()

        temp = ''.join(list)
        sha1 = hashlib.sha1(temp.encode('utf-8'))
        hashcode = sha1.hexdigest()

        print(hashcode, file = sys.stderr)
        
        import sys
        print("handle/GET func: hashcode, signature: ", hashcode, signature, file = sys.stderr)

        if hashcode == signature:
            return make_response(echostr)
        else:
            return ""

api.add_resource(MP_verify, '/MP_verify_ErVytttLPsIDzh7X.txt')
api.add_resource(Token_verify, '/verify/wxtoken')