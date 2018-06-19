#coding=utf-8

import tornado.web
import tornado.httpserver
import tornado.ioloop
import json,os
import time
import torndb
import tornado.options
from tornado.options import options, define
from tornado.web import RequestHandler,StaticFileHandler

class IndexHandler(RequestHandler):
    def get(self):
        # self.set_cookie('c','xjj')
        # # 利用time.mktime将本地时间转换为UTC标准时间
        # self.set_cookie('d','xixi', expires= time.mktime(time.strptime("2018-6-15 23:59:59","%Y-%m-%d %H:%M:%S")))
        # d = self.get_cookie('d')
        # self.write(str(d))
        # self.clear_cookie('d')
        # self.write('hah')

        # 安全Cookie
        self.set_secure_cookie('zhushengjie','ass')
        self.write('haha')

class CountHandler(RequestHandler):
    """统计访问页面的次数 """
    def get(self):
        count = self.get_secure_cookie('count')
        if not count:
            count = 1
            self.set_secure_cookie('count', str(count))
        else:
            count = int(count)+1
            self.set_secure_cookie('count',str(count))
        self.write(str(count))


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexHandler),
            (r'/count', CountHandler),

        ]
        settings = dict(
            static_path=os.path.join(current_path, "static"),
            template_path=os.path.join(current_path, "template"),
            cookie_secret="2hcicVu+TqShDpfsjMWQLZ0Mkq5NPEWSk9fi0zsSt3A=",
        debug=True
        )
        super(Application, self).__init__(handlers,  **settings)
        try:
            self.db =  torndb.Connection(
                host="127.0.0.1",
                database="tornado",
                user="root",
                password="a"
            )
        except Exception as e:
            print(e)


if __name__ == "__main__":
    current_path = os.path.dirname(__file__)

    app = Application()

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(9000)
    tornado.ioloop.IOLoop.current().start()