#coding=utf-8
import os
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import hashlib
import xmltodict 
import time
import json
import tornado.gen
from tornado.web import RequestHandler
from tornado.options import options,define
from tornado.httpclient import AsyncHTTPClient,HTTPRequest


WECHAT_TOKEN = 'zhushengjie'
WECHAT_APPID = "wx16b1c5bc81dbdc31"
WECHAT_APPSECRET = "ea9f6de3c43b777fa434c88877edb8f8"

define("port", default=8000, type=int, help="")


class AccessToken(object):
    """access_token辅助类"""
    _access_token = None
    _expires_in = 0
    _create_time = 0

    @classmethod
    @tornado.gen.coroutine
    def update_access_token(cls):
        #因为发送请求获取access_token是网络IO，有可能阻塞，所以需要用异步客户端
        client = AsyncHTTPClient()
        url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"%(WECHAT_APPID, WECHAT_APPSECRET)
        #有异步客户端就需要协程来协助
        resp = yield client.fetch(url)
        #返回的是json数据，需要转化成python对象
        data = json.loads(resp.body)
        print data
        #判断是否出错，如果有错，则抛出异常，交给调用这个类函数的对象处理
        if "errorcode" in data:
            raise Exception("wechat server error")
        #如果没有出错，则获取access_token并保存
        else:
            cls._access_token = data["access_token"]
            cls._expires_in = data["expires_in"]
            cls._create_time = time.time()
        
    @classmethod
    @tornado.gen.coroutine
    def get_access_token(cls):
        """获取当前时间，计算访问时间，如果大于7000秒，则重新获取access_token,如果小于7000秒则返回access_token"""
        if time.time()-cls._create_time > cls._expires_in-200:
            #只要这个函数中使用了异步函数，就要用yield
            yield cls.update_access_token()
            raise tornado.gen.Return(cls._access_token)
        else:
            #没有超时，直接返回
            raise tornado.gen.Return(cls._access_token)

class QrcodeHandler(RequestHandler):
    """请求微信服务器生成带参数二维码返回给客户"""
    @tornado.gen.coroutine
    def get(self):
        #先获取sid
        scene_id = self.get_argument('sid')
        try:
            #获取access_token
            access_token = yield AccessToken.get_access_token()
        except Exception as e:
            self.write("errmsg: %s" % e)
        else:
            #创建异步客户端获取二维码
            client = AsyncHTTPClient()
            url = "https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=%s" % access_token
            req_data = {"action_name": "QR_LIMIT_SCENE", "action_info": {"scene": {"scene_id": scene_id}}}
            #构建请求内容
            req = HTTPRequest(
                    url=url,
                    method="POST",
                    body = json.dumps(req_data)
            )
            #发送请求
            resp = yield client.fetch(req)
            dict_data = json.loads(resp.body)
            if "errorcode" in dict_data:
                self.write("errmsg:get qrcode error")
            else:
                ticket = dict_data["ticket"]
                qrcode_url = dict_data["url"]
                #回复二维码图片数据
                self.write('<img src="https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=%s"><br/>' % ticket)
                self.write("<p>%s</p>"%qrcode_url)

            


        
class WechatHandler(RequestHandler):
    def prepare(self):
        """对每一个请求进行验证"""

        signature = self.get_argument("signature")
        timestamp = self.get_argument("timestamp")
        nonce = self.get_argument('nonce')
        tmp = [WECHAT_TOKEN, timestamp, nonce]
        tmp.sort()
        tmp = "".join(tmp)
        tmp = hashlib.sha1(tmp).hexdigest()
        if tmp != signature:
            self.send_error(403)


    def get(self):
        """对接微信服务器"""  
        echostr = self.get_argument('echostr')
        self.write(echostr) 
    
    def post(self):
        xml_data = self.request.body
        #将xml文件格式的数据转化为python字典类型的数据
        dict_data = xmltodict.parse(xml_data)
        #获取消息类型
        msg_type = dict_data["xml"]["MsgType"]
        #如果是文本类型，则返回发送过来的数据
        if msg_type == "text":
            content = dict_data["xml"]["Content"]
            print "-----"
            resp_data = {
                "xml":{
                    "ToUserName":dict_data["xml"]["FromUserName"],
                    "FromUserName":dict_data["xml"]["ToUserName"],
                    "CreateTime":int(time.time()),
                    "MsgType":"text",
                    "Content":content,
                    }
            }
            #把字典数据转化成xml格式的数据
            self.write(xmltodict.unparse(resp_data))
           
        elif msg_type == "voice":
            recognition = dict_data["xml"].get("Recognition", u'未识别')
            print dict_data["xml"]
            resp_data = {
                    "xml":{
                        "ToUserName":dict_data["xml"]["FromUserName"],
                        "FromUserName":dict_data["xml"]["ToUserName"],
                        "CreateTime":int(time.time()),
                        "MsgType":"text",
                        "Content":recognition,
                        }
                    }
            self.write(xmltodict.unparse(resp_data))
        elif msg_type == "event":
            if dict_data["xml"]["Event"] == "subscribe":
                resp_data = {
                        "xml":{
                            "ToUserName":dict_data["xml"]["FromUserName"],
                            "FromUserName":dict_data["xml"]["ToUserName"],
                            "CreateTime":int(time.time()),
                            "MsgType":"text",
                            "Content":u"哈喽，我是洪山，感谢关注!",
                            }
                        }
                if "EventKey" in dict_data:
                    #用户未关注时，进行关注后的事件推送
                    eventkey = dict_data["xml"]["EventKey"]
                    sid = eventkey[8:]
                    resp_data["xml"]["Content"] = u"你关注了我哦,%s"%sid
                self.write(xmltodict.unparse(resp_data))
            elif dict_data["xml"]["Event"] == "SCAN":
                #
                sid = dict_data["xml"]["EventKey"]
                resp_data = {
                        "xml":{
                            "ToUserName":dict_data["xml"]["FromUserName"],
                            "FromUserName":dict_data["xml"]["ToUserName"],
                            "CreateTime":int(time.time()),
                            "MsgType":"text",
                            "Content":u"哈喽，你扫描关注了我,%s"%sid
                            }
                        }
                self.write(xmltodict.unparse(resp_data))


        #如果不是文本数据则反回“哈哈，你很皮”
        else:
            print "----------------------------------------"
            resp_data = {
                    "xml":{
                    "ToUserName":dict_data["xml"]["FromUserName"],
                    "FromUserName":dict_data["xml"]["ToUserName"],
                    "CreateTime":int(time.time()),
                    "MsgType":"text",
                    "Content":u"哈哈哈，你很皮欸",
                    }
            }
            self.write(xmltodict.unparse(resp_data))

class ProfileHandler(RequestHandler):
    """微信网页授权"""
    @tornado.gen.coroutine
    def get(self):
        print "hah "
        code = self.get_argument("code")
        client = AcyncHTTPClient()
        url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code"%(WECHAT_APPID,WECHAT_APPSECRET,code)
        resp = yield client.fetch(url)
        dict_data = json.loads(resp.body)
        if "errcode" in dict_data:
            self.write("error occur")
        else:
            access_token = dict_data["access_token"]
            openid = dict_data["openid"]
            url = "https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN"%(access_token, openid)
            resp = yield client.fetch(url)
            user_data = json.loads(resp.data)
            if "errcode" in userdata:
                self.write("error again")
            else:
                self.render("index.html", user = user_data)
            

def main(): 
    tornado.options.parse_command_line()
    app = tornado.web.Application([
       ('/wechat8000', WechatHandler),
       ('/qrcode', QrcodeHandler),
       ('/wechat8000/profile/', ProfileHandler),
       ],
       template_path = os.path.join(os.path.dirname(__file__), "template")  
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__=="__main__":
    main()
                                                                                                                                                                    
                                                                                                                                                                        
