#coding=utf-8
import time
import thread
gen = None

def longio():
    def warpper():
        global gen
        print '开始执行耗时操作'
        time.sleep(5)
        print '结束执行耗时操作'
        try:
            gen.send('io finished')  # # 使用send返回结果并唤醒程序继续执行       
        except StopIteration:   # 捕获生成器完成迭代，防止程序退出
            pass
    thread.start_new_thread(warpper, ())

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
    global gen
    gen = req_a()
    gen.next() # start generator
    req_b()
    while 	1:
        pass
if __name__=='__main__':
    main()

