#coding=utf-8
import time
import thread

def longio(cb):
	def warpper(callback):
		print '开始执行耗时操作'
		time.sleep(5)
		print '结束执行耗时操作'
		result = "io finished"
		callback(result)
	thread.start_new_thread(warpper, (cb, ))

def on_finished(result):
	print "开始执行回掉函数"
	print result	
	print "完成执行回掉函数"



def req_a():
	print "开始执行a"
	longio(on_finished)
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

