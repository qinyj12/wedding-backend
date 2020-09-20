from flask import Blueprint, send_from_directory
from flask.globals import current_app
from flask_restful import Api, Resource
import os

app = Blueprint('invitation', __name__, url_prefix = '/invitation')

api = Api(app)

# 拿到static/dist/index.html
class Invitation(Resource):
    def get(self):
        return send_from_directory(os.path.join(current_app.static_folder, 'dist'), 'index.html')

# 定义一个拿到js、css、jpg、mp3等静态文件的路由
class Invitation_Dependents(Resource):
    def get(self, folder, file):
        return send_from_directory(os.path.join(current_app.static_folder, 'dist', folder), file)

# 拿到static/dist/favicon.ico
class Invitation_favicon(Resource):
    def get(self):
        return send_from_directory(os.path.join(current_app.static_folder, 'dist'), 'favicon.ico')

class Verify(Resource):
    def get(self):
        return current_app.send_static_file('MP_verify_ivOKreMiSvgKkcZC.txt')

api.add_resource(Invitation, '/')
# js、css等静态文件都以二级目录的形式存在于static/dist/js或static/dist/css等文件夹中，
# 所以拿到js文件就是static/dist/js/somejs.js，有2个路由。第一个路由是定位带static/dist/js，第二个路由是定位到somejs.js
api.add_resource(Invitation_Dependents, '/<folder>/<file>')
# static/dist/favicon.ico
api.add_resource(Invitation_favicon, '/favicon.ico')
# 用于公众号JS安全域名验证
api.add_resource(Verify, '/MP_verify_ivOKreMiSvgKkcZC.txt')