# coding:utf-8

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado.options import options, define
from tornado.web import RequestHandler

define("port", default=8000, type=int, help="run server on the given port.")


class IndexRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('my love')

class SubjectRequestHandler(tornado.web.RequestHandler):
    def get(self, a, b):
        """位置参数"""
        self.write('SubjectRequestHandler:%s,%s'%(a,b))


class DataRequestHandler(tornado.web.RequestHandler):
    def get(self, d, c):
        """关键字参数"""
        self.write('DataRequestHandler:%s,%s' % (d, c))


if __name__=='__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application([
        (r"/", IndexRequestHandler),
        (r"/subject/(.+)/([a-z]+)/", SubjectRequestHandler),
        (r'/city/(?P<c>.+)/(?P<d>\d+)/', DataRequestHandler),
    ],debug=True)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
