#coding=utf-8


import tornado.httpserver
import tornado.ioloop
import json,os
import time
import torndb
import tornado.options
from tornado.options import options, define
from tornado.web import RequestHandler,StaticFileHandler
from tornado.httpclient import AsyncHTTPClient

"""
此装饰器用于回调形式的异步方法，并且应该仅用于HTTP的方法上（如get、post等）。
此装饰器不会让被装饰的方法变为异步，而只是告诉框架被装饰的方法是异步的，当方法返回时响应尚未完成。只有在request handler调用了finish方法后，才会结束本次请求处理，发送响应。
不带此装饰器的请求在get、post等方法返回时自动完成结束请求处理。
"""
class IndexHandler(RequestHandler):

    @tornado.web.asynchronous  ## 不关闭连接，也不发送响应,等待http回应
    def get(self):
        httpclient =  AsyncHTTPClient()
        httpclient.fetch("http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=json&ip=14.130.112.24",callback=self.on_response)

    def on_response(self, response):
        json_data = response.body
        data = json.loads(json_data)
        self.write(data.get('city', ''))
        self.finish()  # # 发送响应信息，结束请求处理

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexHandler),
        ]
        settings = dict(
            static_path=os.path.join(current_path, "static"),
            template_path=os.path.join(current_path, "template"),
            debug=True
        )
        super(Application, self).__init__(handlers,  **settings)

        self.db =  torndb.Connection(
                host="127.0.0.1",
                database="tornado",
                user="root",
                password="a"
        )


if __name__ == "__main__":
    current_path = os.path.dirname(__file__)

    app = Application()

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(9000)
    tornado.ioloop.IOLoop.current().start()

