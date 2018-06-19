#coding=utf-8
import time
import thread

def geb_continue(func):
        def inner(*args, **kwargs):
            gen_f = func() #gen_f为生成器req_a
            r = gen_f.next() #r 为生成器longio
            def fun(r):
                ret = r.next() #执行生成器long_io
                try:
                    gen_f.send(ret) #将结果返回给req_a并使其继续执行，返回io finished
                except StopIteration:  # 捕获生成器完成迭代，防止程序退出
                    pass
            thread.start_new_thread(fun, (r,     ))
        return inner

def longio():
    print '开始执行耗时操作'
    time.sleep(5)
    print '结束执行耗时操作'
    yield 'io finished'
    
@geb_continue
def req_a():
    print "开始执行a"
    ret = yield longio()
    print ret
    print "结束执行a"

def req_b():
    print "开始处理请求req_b"
    time.sleep(2) # 添加此句来突出显示程序执行的过程
    print "完成处理请求req_b"

def main():
    req_a()
    req_b()
    while 	1:
        pass
if __name__=='__main__':
    main()


