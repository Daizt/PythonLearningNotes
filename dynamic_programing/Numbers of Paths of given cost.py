# Numbers of Paths of given cost
# Given a M by N matrix A, count number of paths to reach A[M-1][N-1] from
# A[0][0] such that path has given cost.

def path(m,n,M,cost):
	def search(m,n,cost):
		if m == 0 and n == 0:
			if cost == M[m][n]:
				return 1
			else:
				return 0
		elif m == 0:
			return search(m,n-1,cost-M[m][n])
		elif n == 0:
			return search(m-1,n,cost-M[m][n])
		else:
			return search(m,n-1,cost-M[m][n]) + search(m-1,n,cost-M[m][n])

	return search(m,n,cost)

# with lookup table
def path2(m,n,M,cost):
	table = {}
	def search(m,n,cost):
		nonlocal table
		if m == 0 and n == 0:
			if cost == M[m][n]:
				return 1
			else:
				return 0
		key = str(m)+','+str(n)+','+str(cost)
		if key not in table:
			if m == 0:
				table[key] = search(m,n-1,cost-M[m][n])
			elif n == 0:
				table[key] = search(m-1,n,cost-M[m][n])
			else:
				table[key] = search(m,n-1,cost-M[m][n]) + search(m-1,n,cost-M[m][n])
			
		return table[key]
	return search(m,n,cost)
	
def main():
	import time
	import numpy as np
	
	n = 4
	M = [[4,7,1,6],
		 [5,7,3,9],
		 [3,2,1,2],
		 [7,1,6,3],
		]
	cost = 25
	
	# test time complexity
	# n = 12 # matrix dimension
	# M = np.arange(1,n**2+1)
	# M = M.reshape(n,n)
	# np.random.shuffle(M)
	# cost = (n+1)**2
	
	start = time.time()
	num_of_paths = path(n-1,n-1,M,cost)
	end = time.time()
	print("path output:{}, time consumed:{}s".format(num_of_paths,(end-start)))
	
	start = time.time()
	num_of_paths = path2(n-1,n-1,M,cost)
	end = time.time()
	print("path2 output:{}, time consumed:{}s".format(num_of_paths,(end-start)))
	
if __name__ == "__main__":
	main()