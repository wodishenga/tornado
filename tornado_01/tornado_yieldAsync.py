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
import tornado.gen.coroutine

class IndexHandler(RequestHandler):

    # @tornado.web.coroutine
    # def get(self):
    #     httpclient =  AsyncHTTPClient()
    #     response = yield httpclient.fetch("http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=json&ip=14.130.112.24",callback=self.on_response)
    #     json_data = response.body
    #     data = json.loads(json_data)
    #     self.write(data.get('city', ''))

    """
    
    """
    @tornado.web.coroutine
    def get(self):
        city = yield self.get_ip_city()
        self.write(city)

    @tornado.web.coroutine
    def get_ip_city(self):
        httpclient =  AsyncHTTPClient()
        response = yield httpclient.fetch("http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=json&ip=14.130.112.24",callback=self.on_response)
        json_data = response.body
        data = json.loads(json_data)
        raise tornado.gen.Return(data.get('city', ''))


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

