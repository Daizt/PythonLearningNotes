# Matrix Chain Multiplication Cost
# c[i,j] denotes the minimum cost by multiply M[i]M[i+1]...M[j]

def Cost(dim):
	N = len(dim) # matrix nums
	c = [[0 for _ in range(N)] for _ in range(N)]
	for lens in range(2,N+1): 
		for i in range(N-lens+1):
			j = i+lens-1
			c[i][j] = 1e10
			for k in range(i,j): # divide
				cost = c[i][k] + c[k+1][j] + dim[i][0]*dim[k][1]*dim[j][1]
				if cost < c[i][j]:
					c[i][j] = cost
	return c
	
def main():
	dim = [[10,30],[30,5],[5,60],[60,2]] # dimensions of three matrices
	c = Cost(dim)
	print("minimum cost is {}".format(c[0][len(dim)-1]))
	
if __name__ == "__main__":
	main()