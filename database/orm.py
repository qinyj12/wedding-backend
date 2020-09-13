from sqlalchemy import Column, String, Integer, create_engine, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime

def initialize_orm():
    Base = declarative_base()

    # 评论列表
    class Comments(Base):
        __tablename__ = 'comments'
        id = Column(Integer, primary_key = True, nullable = False)
        content = Column(String(20), nullable = False)
        time = Column(String(20), default = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), nullable = False)

    # 这里要注意路径是database/database.db
    engine = create_engine('sqlite:///database/database.db', connect_args = {'check_same_thread': False})
    DBSession = sessionmaker(engine)
    session = DBSession()

    return {'session': session, 'comments': Comments}

    # return Base.metadata.create_all(engine)