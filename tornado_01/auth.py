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

    def get_current_user(self):
        """如果没有登陆成功，则跳转到登陆页面"""
        f = self.get_argument('f',None )
        if f:
            return True
        else:
            return False


    @tornado.web.authenticated
    def get(self):
        self.write('hah')


class LoginHandler(RequestHandler):
    def get(self):
        next_url = self.get_argument('next', '')
        if next_url:
            """跳转到原登录页面"""
            self.redirect(next_url+'?f=login')
        else:
            self.write("logined")

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexHandler),
            (r'/login', LoginHandler),

        ]
        settings = dict(
            static_path=os.path.join(current_path, "static"),
            template_path=os.path.join(current_path, "template"),
            cookie_secret="2hcicVu+TqShDpfsjMWQLZ0Mkq5NPEWSk9fi0zsSt3A=",
            login_url = '/login',
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

