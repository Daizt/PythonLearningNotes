import argparse

parser = argparse.ArgumentParser(description='"The Description of the Program."')	
parser.add_argument('-n', '--number', help='The number of the plates in hano.',
					type=int)

args = parser.parse_args()

		
#     递归与闭包：闭包避免了使用全局变量，此外，闭包允许将函数与其所操作的某些数据（环境）关连起来。
# 这一点与面向对象编程是非常类似的，在面向对象编程中，对象允许我们将某些数据（对象的
# 属性）与一个或者多个方法相关联。
#     注意：每次调用hano()都会产生一个新的函数，其id并不相同。
def test1(n):
	count = 0

	def hano(n,a='a',b='b',c='c'):
		nonlocal count # 使用时需要在外部声明一个变量count=0
		# global count # 此句对应于在最外层声明的全局变量
		assert isinstance(n, int) and n > 0
		if n == 1:
			print(a,'-->',c)
			count += 1
		else:
			hano(n-1,a,c,b)
			hano(1,a,b,c)
			hano(n-1,b,a,c)
		return count
	
	result = hano(n)
	print("{} plates, {} moves. ".format(n,result))
	
#     这里使用闭包在无需使用外部变量的前提下实现了对于移动次数的计算。闭包类似于类方法，可以
# 将父函数的参数或变量保留下来并继承给子函数。
def test2(n):
	def hano2(n):
		count = 0
		assert isinstance(n, int) and n > 0
		def move(n=n,a='a',b='b',c='c'):
			nonlocal count # 子函数可以访问父函数的变量，但是不可以修改；这里nonlocal使得子函数可以修改父函数中的变量
			if n == 1:
				print(a,'-->',c)
				count += 1
			else:
				move(n-1,a,c,b)
				move(1,a,b,c)
				move(n-1,b,a,c)
			return count
		return move
	result = hano2(n)()
	print("{} plates, {} moves. ".format(n,result))

# 闭包：将子函数的算法、连同子函数计算过程中需要用到的父函数中的局部变量或参数打包在一起的算法与操作数集合。
# 闭包详解：调用count()产生三个闭包，而三个闭包共用一个操作数i，故i作为闭包的内容被保留在内存中。在完成三个闭包时i的值
# 为3，故而三个子函数最终的计算结果都为3*3=9.
def test3():
	def count():
		fs = []
		for i in range(1, 4):
			def f():
				 return i*i
			fs.append(f)
		return fs

	f1, f2, f3 = count()
	print(f1(),f2(),f3()) # 9 9 9
	
# 闭包详解：同样产生三个闭包，但不同的是三个闭包使用三个独立的操作数（j），在产生闭包的过程中其各自的操作数就已经有了确定的
# 值1、2、3，所以最终的计算结果为1 4 9.
def test4():
	def count():
		def f(j):
			def g():
				return j*j
			return g
		fs = []
		for i in range(1, 4):
			fs.append(f(i)) # f(i)立刻被执行，因此i的当前值被传入f()
		return fs
	f1, f2, f3 = count()
	print(f1(),f2(),f3()) # 1 4 9

# 闭包详解：仿照上例，为每个闭包分配一个独立的操作数j，在产生闭包时各个闭包的操作数都已有了明确的值。
def test5():
	def count():
		fs = []
		for i in range(1, 4):
			def f(j=i):
				 return j*j
			fs.append(f)
		return fs

	f1, f2, f3 = count()
	print(f1(),f2(),f3()) # 1 4 9

# 闭包详解：先分析闭包结构，三个闭包共用一个操作数i，但不同的是每个闭包使用nonlocal声明获得了i的改动权，在闭包产生完毕时i
# 的值为3，当计算第一个闭包f1时，f1将i改为了4所以结果为16；f2运算时得到的i为4，以此类推。
def test6():	
	def count():
		fs = []
		for i in range(1, 4):
			def f():
				nonlocal i
				print(i)
				i = i+1
				print(i)
				return i*i
			fs.append(f)
		return fs

	f1, f2, f3 = count()
	print(f1(),f2(),f3()) # 16 25 36
	
# generator的运行过程：在yield处中断，下次从中断处执行。
def test7():
	def triangles():
		n = 1
		l_1 = [1]
		l_2 = [1, 1]
		while True:
			if n == 1:
				yield l_1
			elif n == 2:
				yield l_2
			else:
				l_1,l_2 = l_2,[1 for i in range(n)]
				for i in range(1,n-1):
					l_2[i] = l_1[i-1] + l_1[i]
				yield l_2
				l_1 = l_2
			n += 1
	n = 0
	results = []
	for t in triangles():
		print(t)
		results.append(t)
		n = n + 1
		if n == 10:
			break
	if results == [
		[1],
		[1, 1],
		[1, 2, 1],
		[1, 3, 3, 1],
		[1, 4, 6, 4, 1],
		[1, 5, 10, 10, 5, 1],
		[1, 6, 15, 20, 15, 6, 1],
		[1, 7, 21, 35, 35, 21, 7, 1],
		[1, 8, 28, 56, 70, 56, 28, 8, 1],
		[1, 9, 36, 84, 126, 126, 84, 36, 9, 1]
	]:
		print('测试通过!')
	else:
		print('测试失败!')

# filter 的用法：为真保留，为假去除。
def test8():

	def is_palindrome(n):
		s = str(n)
		if len(s) == 1:
			return True
		else:
			for i in range(int(len(s)/2)):
				if s[i] != s[len(s)-i-1]:
					return False
			return True
	output = filter(is_palindrome, range(1,1000))
	print('1~1000:', list(output))
	if list(filter(is_palindrome, range(1, 200))) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 22, 33, 44, 55, 66, 77, 88, 99, 101, 111, 121, 131, 141, 151, 161, 171, 181, 191]:
		print('测试成功!')
	else:
		print('测试失败!')
		
# decorator
def test9():
	import time,functools
	def metric(func):
		@functools.wraps(func) # 此句使得被装饰的函数名称不变
		def wrapper(*args,**kw):
			print('{:s} executed in {:s} ms'.format(func.__name__, '10.24'))
			return func(*args,**kw)
		return wrapper
		
	@metric
	def fast(x, y):
		time.sleep(0.0012)
		return x + y;

	@metric
	def slow(x, y, z):
		time.sleep(0.1234)
		return x * y * z;

	f = fast(11, 22)
	s = slow(11, 22, 33)
	if f != 33:
		print('测试失败!')
	elif s != 7986:
		print('测试失败!')
	
	print(fast.__name__)
	
# 错误处理
def test10():
	def foo(s):
		return 10 / int(s)

	def bar(s):
		return foo(s) * 2

	def main():
		try:
			bar('0')
		except Exception as e:
			print('Error:', e)
		finally:
			print('finally...')
	
# 使用assert（断言）检查条件真伪性
def test11():
	def foo(s):
		n = int(s)
		assert n != 0, 'n is zero!'
		return 10 / n

	def main():
		foo('0')
		
	main()

# 使用pdb调试器
def test12():
	import pdb
	s = '0'
	n = int(s)
	pdb.set_trace() # 设置断点，输入c继续运行
	print(10 / n)

# 文件读写
def test13():
	import os
	import linecache
	
	path = os.getcwd() # 或者os.path.abspath('.')
	file = os.path.join(path, 'file.txt')

	with open(file, 'w') as f: # 以这种方式写入会清除原始文件内容，若无此文件则创建一个文件
		s = '0123456789ABCDEFG#writing to file...\n'
		f.write(s)
		
	with open(file, 'a') as f: # 以这种方式写入会在原文件内容末尾添加新内容
		s = 'appending a new line...\n'
		f.write(s)
		f.write('123ending\n')
		
	with open(file, 'r') as f: # 只读模式，‘rb'表示按二进制方式读取
		print(f.tell()) # 输出读取位置
		print(f.read(5)) # 从头读取5个字符
		print(f.tell())
		print(f.read(5)) # 接着读取5个字符
		print(f.readline()) # 接着读取一行
		print(f.readlines()) # 接着读取剩余行并返回列表
		
	with open(file, 'rb') as f: # 注：'r'只支持feek(offset,0)模式
		f.seek(5,0) # f.seek(offset, start),0:从头开始,5:后移5个字符位
		print(f.read(2))
		f.seek(2,1) # 1:从当前位置开始,2:后移两个字符位
		print(f.read(1))
		f.seek(-2,1) # 1:从当前位置开始 -2：前移两个字符位
		print(f.read(1))
		f.seek(-4,2) # 2:从末尾开始，-3：前移3个字符位
		print(f.read(2))
		
	line1 = linecache.getlines(file) # 读取全部行并返回列表
	# line1 = linecache.getlines(file)[1:15] # 读取1~15行并返回列表
	line2 = linecache.getline(file, 1) # 读取指定行
	print('line1: ', line1)
	print('line2: ', line2)
	
if __name__ == '__main__':
	test13()