class Config(object):
    # 开启debug模式
    DEBUG = True
    # 非ASCII编码不要转义
    RESTFUL_JSON = {'ensure_ascii': False}
    # 缓存对象使用的类型
    CACHE_TYPE = "simple"
    
    # 微信公众号安全域名：本地测试
    # WX_SECURITY_DOMAIN = 'http://192.168.1.6:5000'
    # 微信公众号安全域名：服务器
    WX_SECURITY_DOMAIN = 'http://wedding.southdog.cool'

