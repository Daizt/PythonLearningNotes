# Longest Common Substring
# 最长公共子串问题（连续的子列）
# LCS[i,j] 表示以a[i],b[j]结尾的最长公共子串的长度，则它仅与LCS[i-1,j-1]有关

def LCS(a,b):
	m,n = len(a),len(b)
	lcs = [[0 for _ in range(n+1)] for _ in range(m+1)]
	for i in range(1,m+1): #注意此处的j，j表示的使lcs矩阵的索引
		for j in range(1,n+1):
			if a[i-1] == b[j-1]:
				lcs[i][j] = lcs[i-1][j-1] + 1
			else:
				lcs[i][j] = 0
	return lcs
	
def findLCS(a,b,lcs):
	max_v = max([max(x) for x in lcs])
	ith = [i for i,j in enumerate(lcs) if max(j) == max_v]
	# jth = [j for i in ith for j,v in enumerate(lcs[i]) if v == max_v ]
	res = []
	for a_i in ith: # 注意此索引为lcs表中的索引，大于序列a的对应索引
		res.append("")
		for i in range(max_v):
			res[-1] = a[a_i - 1 - i] + res[-1]
	return res

def main():
	a = "ABAB"
	b = "BABA"
	lcs = LCS(a,b)
	max_length = max([max(x) for x in lcs])
	res = findLCS(a,b,lcs)
	print("max_length: {}".format(max_length))
	print(res)
	
if __name__ == "__main__":
	main()