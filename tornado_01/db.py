#coding=utf-8

import tornado.web
import tornado.httpserver
import tornado.ioloop
import json,os
import torndb
import tornado.options
from tornado.options import options, define
from tornado.web import RequestHandler,StaticFileHandler

class IndexHandler(RequestHandler):
    def get(self):
        ret = self.application.db.get('select ui_name,ui_age from it_user_info  where ui_user_id =1')
        print(ret) #{'ui_name': u'xixi', 'ui_age': 20L}
        print(type(ret))
        self.write(ret['ui_name'])

class InsertHandler(RequestHandler):
    def get(self):
        user_id = None
        name = self.get_argument('name')
        passwd = self.get_argument('passwd')
        mobile = self.get_argument('mobile')
        sql = "insert into it_user_info(ui_name,ui_passwd,ui_mobile) values(%(name)s,%(passwd)s,%(mobile)s)"
        try:
            user_id =  self.application.db.execute(sql,name=name,passwd=passwd,mobile=mobile)
        except Exception as e:
            print(e)
            self.write("DB:error :%s"%e)
        print type(user_id) #返回影响的最后一条自增字段值   ui_user_id
        self.write(str(user_id))

class queryHandler(RequestHandler):
    def get(self):
        ret = None
        uid = self.get_argument('uid')
        sql = "select ui_name, hi_name, hi_price from it_house_info inner  join it_user_info on hi_user_id=ui_user_id where ui_user_id=%s"
        try:
            ret = self.application.db.query(sql, uid)
        except Exception  as e:
            print e
            return self.write({'erron':1, 'err_msg':'db err','data':e})
        print type(ret)
        # [{'hi_price': 30000L, 'hi_name': u'haha\u7684\u623f\u5b50', 'ui_name': u'haha'}, {'hi_price': 50000L, 'hi_name': u'haha\u7684\u623f\u5b50b', 'ui_name': u'haha'}]
        print ret
        houses = []
        if ret:
            for l in ret:
                house  =  {
                      "uname":l["ui_name"],
                      "hname":l['hi_name'],
                      "hprice":l['hi_price']
                }
                houses.append(house)
        self.write({'erron': 0, 'err_msg': 'OK', 'data': houses})


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexHandler),
            (r'/insert', InsertHandler),
            (r'/query', queryHandler)
        ]
        settings = dict(
            static_path=os.path.join(current_path, "static"),
            template_path=os.path.join(current_path, "template"),
            debug=True
        )
        super(Application, self).__init__(handlers,  **settings)
        try:
            self.db =  torndb.Connection(
                host="127.0.0.1",
                database="tornado",
                user="root",
                password="a"
            )
        except Exception as e:
            print(e)


if __name__ == "__main__":
    current_path = os.path.dirname(__file__)

    app = Application()

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(9000)
    tornado.ioloop.IOLoop.current().start()