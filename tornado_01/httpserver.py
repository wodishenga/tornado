#coding=utf-8

import tornado.web
import tornado.ioloop
import tornado.httpserver

#RequestHandler携带了http请求的参数
class IndexAppliaction(tornado.web.RequestHandler):
    """主路由处理类"""
    def get(self):
        """对应http的get请求方式"""
        self.write('hello world')

if __name__=="__main__":
    #创建一个应用
    app = tornado.web.Application([(r'/', IndexAppliaction)])
    # 创建了一个tornado自带的http服务器，
    # 让这个服务器服务于这个应用，将接收到的客户端请求通过web应用中的路由映射表引导到对应的handler中
    http_server = tornado.httpserver.HTTPServer(app)
    # http_server.listen(8000)  # 默认开启一个进程

    #=0，开启与cpu核心数相等的子进程数，默认值为1，如果>0,创建num_processes个子进程。
    http_server.bind(8000)
    http_server.start(0)

    #进入事件循环并启动监听 ，当有io操作时，将http的参数传给url，再通过Application匹配，交给IndexHandler处理
    tornado.ioloop.IOLoop.current().start()