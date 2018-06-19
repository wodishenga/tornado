#coding=utf-8

import tornado.web
import tornado.httpserver
import tornado.ioloop
import json
import tornado.options
from tornado.options import options, define
from tornado.web import RequestHandler

class IndexHandler(tornado.web.RequestHandler):
    # def prepare(self):
    #     if self.request.headers.get('Content-Type').startswith('application/json'):
    #         """预处理，即在执行对应请求方式的HTTP方法（如get、post等）前先执行，注意：不论以何种HTTP方式请求，都会执行prepare()方法。"""
    #         #通过反序列化把字符串转换成list or dict
    #         #外形不是list或者dict的形状，则不会转换成功的,
    #         # 这里必须要注意，字符串的外面的引号必须是“单引号”，内部必须是双引号，如果不是这样，json模块会报错的
    #         self.json_dict =  json.load(self.request.body)
    #     else:
    #         self.json_dict = None
    #
    # def post(self):
    #     for key,value in self.json_dict.items():
    #         self.write("<h3>%s</h3><p>%s</p>" % (key, value))
    #
    # def put(self):
    #     for key, value in self.json_dict.items():
    #         self.write("<h3>%s</h3><p>%s</p>" % (key, value))
    def initialize(self):
        print "调用了initialize()"

    def prepare(self):
        print "调用了prepare()"

    def set_default_headers(self):
        print "调用了set_default_headers()"

    def write_error(self, status_code, **kwargs):
        print "调用了write_error()"

    def get(self):
        print "调用了get()"

    def post(self):
        print "调用了post()"
        self.send_error(200)  # 注意此出抛出了错误

    def on_finish(self):
        print "调用了on_finish()"


if __name__ == "__main__":
    app = tornado.web.Application([
        (r'/', IndexHandler),
    ],debug=True)

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8000)
    tornado.ioloop.IOLoop.current().start()

"""
调用了set_default_headers()
调用了initialize()
调用了prepare()
调用了get()
调用了on_finish()
"""
"""
调用了set_default_headers()
调用了initialize()
调用了prepare()
调用了post()
调用了set_default_headers()  #因为出错了，所以充值头部
调用了write_error()
调用了on_finish()
"""