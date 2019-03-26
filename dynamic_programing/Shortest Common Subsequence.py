# Shortest Common Subsequence
# 最短公共父列
# SCS[i,j] denotes the length of SCS of a[0:i] and b[0:j]

def SCS(a,b):
	m,n = len(a),len(b)
	scs = [[0 for _ in range(n+1)] for _ in range(m+1)]
	scs[0] = list(range(n+1))
	
	for i in range(m+1):
		scs[i][0] = i

	for i in range(1,m+1):
		for j in range(1,n+1):
			if a[i-1] == b[j-1]:
				scs[i][j] = scs[i-1][j-1] + 1
			else:
				scs[i][j] = min(scs[i-1][j]+1,scs[i][j-1]+1)
	return scs

def main():
	a = "ABCBDAB"
	b = "BDCABA"
	scs = SCS(a,b)
	print("the length of SCS is {}".format(scs[len(a)][len(b)]))

if __name__ == "__main__":
	main()