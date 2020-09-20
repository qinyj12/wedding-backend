from flask import Blueprint, abort
from flask_restful import Api, Resource, reqparse, fields
from database import orm

app = Blueprint('comment', __name__, url_prefix = '/comment')
api = Api(app)
parser = reqparse.RequestParser()
database_orm = orm.initialize_orm()
database_session = database_orm['session']
database_comments = database_orm['comments']

class Comment(Resource):
    # 查
    def get(self):
        # database_comments.id.desc()根据id倒序排序
        # [0: 3]切片
        all_comments = database_session.query(database_comments).order_by(database_comments.id.desc())[0: 30]
        return [comment.content for comment in all_comments]
    # 增
    def post(self):
        # 从'form'中拿到提交的数据
        parser.add_argument('comment', type = str, location = 'form')
        args = parser.parse_args()
        arg_comment = args['comment']
        # 组合成新的值，用于插入数据库
        new_comment  = database_comments(
            content = arg_comment
        )
        # 存入数据库
        database_session.add(new_comment)
        try:
            database_session.commit()
            database_session.close()
            return '记录成功'
        except Exception as e:
            database_session.rollback()
            database_session.close()
            return str(e), 500

api.add_resource(Comment, '/')