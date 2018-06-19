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
        self.render('zhuanyi.html', text='')

    def post(self):
        text = self.get_argument('text', '')
        print(text)
        #默认是进行转义的，防止注入攻击
        self.render('zhuanyi.html', text=text)


if __name__ == "__main__":
    current_path = os.path.dirname(__file__)
    app = tornado.web.Application([
        (r'/', IndexHandler),
        (r'/(.*)', StaticFileHandler, {"path":os.path.join(current_path,'static/html/'),
         "default_filename":"index.html"}),
        ],
        static_path =os.path.join(current_path, "static"),
        template_path = os.path.join(current_path, "template"),
        debug=True)

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8000)
    tornado.ioloop.IOLoop.current().start()