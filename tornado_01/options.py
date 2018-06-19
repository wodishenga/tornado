#coding=utf-8

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options

from tornado.options import  define,options
from tornado.web import   RequestHandler,url

tornado.options.define('port', default=8000, type=int, help='run server on given port')
tornado.options.define('zhushengjie', default=[], type=str, help='test')

#RequestHandler携带了http请求的参数
class IndexAppliaction(tornado.web.RequestHandler):
    """主路由处理类"""
    def get(self):
        """对应http的get请求方式"""
        #调用RequestHandler.reverse_url(name)来获取cpp_url对应的url
        self.write('<a href="'+ self.reverse_url('cpp_url')+'">cpp</a>')

class SubjectHandler(tornado.web.RequestHandler):
    def initialize(self, subject):
        """为每个请求调用。作为URL规范的第三个参数传递的字典将会是作为关键字参数提供给initialize（）。"""
        self.subject = subject

    def get(self):
        self.write(self.subject)


if __name__=="__main__":
    #创建一个应用
    tornado.options.parse_command_line()
    print tornado.options.options.port
    print tornado.options.options.zhushengjie

    app = tornado.web.Application([
        (r'/', IndexAppliaction),
        (r'/python',SubjectHandler, {'subject':'python'}),
        url(r'/cpp', SubjectHandler, {'subject':'cpp'}, name='cpp_url'),
        ],
        #当debug=True时，运行程序时当有代码、模块发生修改，程序会自动重新加载
        debug=True
        )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8000)  # 默认开启一个进程

    tornado.ioloop.IOLoop.current().start()