# 工厂函数从cache.py引用，视图函数从cache.py里引用，这样就不会循环引用了
from flask_caching import Cache

cache = Cache()