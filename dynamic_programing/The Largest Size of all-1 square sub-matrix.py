# The Largest Size of all-1 square sub-matrix
# In this problem, L[i,j] denotes the size of the largest all-1 square sub-matrix
# that ends with a[i][j]

def findSize(a):
	m,n = len(a),len(a[0])
	L = [[0 for _ in range(n)] for _ in range(m)]
	for i in range(m):
		for j in range(n):
			if a[i][j] == 1:
				L[i][j] = min(L[i-1][j],L[i][j-1],L[i-1][j-1]) + 1
			else:
				L[i][j] = 0
	return L
	
def main():
	a = [[0,0,1,0,1,1],
		 [0,1,1,1,0,0],
		 [0,0,1,1,1,1],
		 [1,1,0,1,1,1],
		 [1,1,1,1,1,1],
		 [1,1,0,1,1,1],
		 [1,0,1,1,1,1],
		 [1,1,1,0,1,1],
		]
	L = findSize(a)
	maxSize = max([max(x) for x in L])
	print("The largest size is {}".format(maxSize))

if __name__ == "__main__":
	main()