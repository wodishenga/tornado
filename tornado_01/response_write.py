#coding=utf-8

import tornado.web
import tornado.httpserver
import tornado.ioloop
import json
import tornado.options
from tornado.options import options, define
from tornado.web import RequestHandler

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        """"""
        # self.write("xixi") # 只是暂存到了缓冲区，还没有输出到浏览器
        # self.write("xixi")
        # self.write("xixi")

        data = {"name":"hehe","age":24,"gender":1}
        #self.write(data)#Write会自动的把字典类型的数据转化为json格式传输
        json_data = json.dumps(data)

        self.write(json_data)
        self.set_header('Content-Type','application/json; charset=UTF-8')

if __name__ == "__main__":
    app = tornado.web.Application([
        (r'/', IndexHandler),
    ],debug=True)

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8000)
    tornado.ioloop.IOLoop.current().start()