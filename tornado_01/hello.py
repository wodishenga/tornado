#coding=utf-8

import tornado.web
import tornado.ioloop

#RequestHandler携带了http请求的参数
class IndexAppliaction(tornado.web.RequestHandler):
    """主路由处理类"""
    def get(self):
        """对应http的get请求方式"""
        self.write('hello world')

if __name__=="__main__":
    #创建一个应用
    app = tornado.web.Application([(r'/', IndexAppliaction)])
    # 创建了一个http服务器, 绑定端口，并没有监听
    #app.listen()这个方法只能在单进程模式中使用
    app.listen(8000)
    #进入事件循环并启动监听 ，当有io操作时，将http的参数传给url，再通过Application匹配，交给IndexHandler处理
    tornado.ioloop.IOLoop.current().start()

