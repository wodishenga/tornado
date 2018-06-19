#coding=utf-8

import tornado.web
import tornado.httpserver
import tornado.ioloop
import json
import tornado.options
from tornado.options import options, define
from tornado.web import RequestHandler

class IndexHandler(RequestHandler):
    def set_default_headers(self):
        print "执行了set_default_headers()"
        # 设置get与post方式的默认响应体格式为json
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        # 设置一个名为hehe、值为python的header
        self.set_header("hehe", "python")

    def get(self):
        print "执行了get()"
        stu = {
            "name":"zhangsan",
            "age":24,
            "gender":1,
        }
        stu_json = json.dumps(stu)
        self.write(stu_json)
        self.set_header("hehe", "i love python") # 注意此处重写了header中的itcast字段
        self.set_status(211,'error')
    def post(self):
        print "执行了post()"
        stu = {
            "name":"zhangsan",
            "age":24,
            "gender":1,
        }
        stu_json = json.dumps(stu)
        self.write(stu_json)

class redirectHandler(RequestHandler):

    def get(self):
        """重定向"""
        print('redirect')
        self.redirect('/')

if __name__ == "__main__":
    app = tornado.web.Application([
        (r'/', IndexHandler),
        (r'/redirect/',redirectHandler)
    ],debug=True)

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8000)
    tornado.ioloop.IOLoop.current().start()