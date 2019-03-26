# The Levenshtein Distance (Edit Distance)
# 编辑距离描述了两字符串a、b的相似程度，它表示将a转化为b所需的最小操作数
# （删除、插入或代替的次数）。

def dist(a,b):
	m,n = len(a),len(b)
	d = [[0 for _ in range(n+1)] for _ in range(m+1)]
	d[0] = list(range(n+1))
	for i in range(m+1):
		d[i][0] = i
	for i in range(1,m+1):
		for j in range(1,n+1):
			if a[i-1] == b[j-1]:
				d[i][j] = d[i-1][j-1]
			else:
				d[i][j] = min(d[i-1][j],d[i][j-1],d[i-1][j-1])
				d[i][j] += 1
	return d
	
def main():
	a = "kitten"
	b = "sitting"
	d = dist(a,b)
	print("edit distance is {}".format(d[len(a)][len(b)]))

if __name__ == "__main__":
	main()