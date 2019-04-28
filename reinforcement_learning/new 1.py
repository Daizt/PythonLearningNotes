import numpy as np

a = 5

def Q(a):
	def f(n):
		print(a)
		res = a + n
		return res
	return f

f = Q(a)
print("a = {}, f(1) = {}".format(a, f(1)))
a += 1
print("a = {}, f(1) = {}".format(a, f(1)))

