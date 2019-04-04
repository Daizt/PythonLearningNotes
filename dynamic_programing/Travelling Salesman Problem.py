# Travelling Salesman Problem
# Using DP: C(S,i) denotes the cost of minimum cost path visiting each vertex in 
# set S exactly once, starting at 0 ending at i(Note that i belongs to S). Thus the
# anwer to our problem is C(S,0), where S contains all the given cities. 

def shortestPathDP(pos):
	pos = [0,0] + pos
	N = len(pos)//2
	D = [[0 for _ in range(N)]for _ in range(N)]
	for i in range(N):
		for j in range(i+1,N):
			dist = ((pos[i*2]-pos[j*2])**2+(pos[i*2+1]-pos[j*2+1])**2)**0.5
			D[i][j] = D[j][i] = dist
	def C(S,i):
		if len(S) == 1:
			return D[0][i]
		else:
			return min([C(S-{i},k) + D[k][i] for k in S-{i}])
	S = set(list(range(N)))
	return C(S,0)

def main():
	pos = [200,0,200,10,200,50,200,30,200,25]
	res = shortestPathDP(pos)
	print(res)
	
if __name__ == "__main__":
	main()