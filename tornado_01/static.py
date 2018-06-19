#coding=utf-8

import tornado.web
import tornado.httpserver
import tornado.ioloop
import json,os
import tornado.options
from tornado.options import options, define
from tornado.web import RequestHandler,StaticFileHandler

class IndexHandler(RequestHandler):
    def get(self):
        self.render('index.html', p1=100, p2=200)

class xixiHandler(RequestHandler):
    def get(self):
        self.write("xiix")

if __name__ == "__main__":
    current_path = os.path.dirname(__file__)
    settings = dict(
        static_path=os.path.join(current_path, "static"),
        template_path=os.path.join(current_path, "template"),
        debug=True
    )
    app = tornado.web.Application([
        (r'/', IndexHandler),
        (r'/xixi', xixiHandler),
        (r'/(.*)', StaticFileHandler, {"path":os.path.join(current_path,'static/html/'),
         "default_filename":"index.html"}),
        ],**settings
 )

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8000)
    tornado.ioloop.IOLoop.current().start()