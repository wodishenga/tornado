#coding=utf-8

import tornado.web
import tornado.ioloop
import tornado.httpserver

from tornado.web import RequestHandler,url

class IndexAppliaction(tornado.web.RequestHandler):
    def post(self):
        #没有设置默认值，没有相对应的键传入那么抛出异常
        #query_arg  = self.get_query_argument("a",default='haha')
        #query_args = self.get_query_arguments('b')
        #print type(query_args) #list
        #body_arg = self.get_body_argument('a')
        #body_args = self.get_body_arguments('a')
        #arg = self.get_argument('a')
        #接收任意参数
        args = self.get_arguments('a')
        print self.request.method
        print self.request.host
        print self.request.headers.get('Content-type')
        print self.request.body

        self.write(str(args))



if __name__=='__main__':
    app = tornado.web.Application([
        (r'/', IndexAppliaction)
        ],debug=True)
    httpserver = tornado.httpserver.HTTPServer(app)
    httpserver.listen(8000)

    tornado.ioloop.IOLoop.current().start()
