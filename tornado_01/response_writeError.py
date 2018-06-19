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
        err_code = self.get_argument("code", None) # 注意返回的是unicode字符串，下同
        err_title = self.get_argument("title", "")
        err_content = self.get_argument("content", "")
        if err_code:
            self.send_error(err_code, title=err_title, content=err_content)
        else:
            self.write("主页")

    def write_error(self, status_code, **kwargs):
        """用来处理send_error抛出的错误信息并返回给浏览器错误信息页面"""
        self.write(u"出错了<br/>")
        self.write(u"%s<br/>"%kwargs["title"])
        self.write(u"%s<br/>"%kwargs["content"])
        #kwargs["title"] 是unicode字符串, 出错了<br/>是 普通字符串assic , 要搞成编码格式一样才行


if __name__ == "__main__":
    app = tornado.web.Application([
        (r'/', IndexHandler),
    ],debug=True)

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8000)
    tornado.ioloop.IOLoop.current().start()