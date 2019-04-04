# Maximize the Value of given expression
# Given an array A, maximize the value of the expression (A[s]-A[r]+A[q]-A[p]),
# where s>r>r>p are indices of A.

def Maximize(A):
	def f(start,end):
		if end-start < 4:
			return -1e10
		elif end-start == 4:
			p,q,r,s = list(range(start,end))
			return A[s]-A[r]+A[q]-A[p]
		else:
			return max([f(start+offset,end+offset) for offset in range(end-start-4+1)])
	
	start,end = 0,len(A)-1
	return f(start,end)
	
def main():
	A = [3,9,10,1,30,40]
	res = Maximize(A)
	print("maximum value: {}".format(res))
	
if __name__ == "__main__":
	main()