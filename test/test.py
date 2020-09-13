class Demo:
    def __init__(self, arg):
        self.arg = arg
    # 用print调用
    def __repr__(self):
        # %r是把参数原样打印出来，这里用%s其实也是可以的
        return 'Demo(%r)' % (self.arg)

    def __demo__(self):
        return str(self.arg) + 'YES'

temp = [Demo(1), Demo(2)]

print(list(i.__demo__() for i in temp))