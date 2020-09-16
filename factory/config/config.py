class Config(object):
    # 开启debug模式
    DEBUG = True
    # 非ASCII编码不要转义
    RESTFUL_JSON = {'ensure_ascii': False}
    # 缓存对象使用的类型
    CACHE_TYPE = "simple"