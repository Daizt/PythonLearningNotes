# Longest Common Subsequence
# 最长公共子列问题
# LCS[i,j] denotes the length of the longest common subsequence of a[0:i] and b[0:j]

def LCS(a,b):
	m, n = len(a),len(b)
	lcs = [[0 for _ in range(n+1)] for _ in range(m+1)]
	for i in range(1,m+1):
		for j in range(1,n+1):
			if a[i-1] == b[j-1]:
				lcs[i][j] = lcs[i-1][j-1] + 1
			else:
				lcs[i][j] = max(lcs[i-1][j],lcs[i][j-1])
	return lcs

def FindLCS(lcs,a,b):
	# 注意：此处的a对应lcs表的行方向，b对应列方向
	res = [""]
	a,b = '0'+a,'0'+b # 此处是为了使得原a、b的字符位与lcs表格对齐
	m,n = len(a)-1,len(b)-1
	def find(res,i,j,k):
		# res 存储所有LCS
		# i, j 表示当前在lcs表格中的位置
		# k 表示解的索引
		if i < 1 or j <1:
			return 
		if a[i] == b[j]:
			res[k] = a[i] + res[k] 
			if i == 1 or j == 1: # 完善退出条件，避免某一字符串首字符多次与另一字符串匹配
				return

		# 在lcs表格中回溯
		if lcs[i][j] == lcs[i-1][j] and lcs[i][j] == lcs[i][j-1]: # 多解
			res.append(res[k]) # 增加一个解 
			find(res,i-1,j,k)
			find(res,i,j-1,len(res)-1)
		
		elif lcs[i][j] == lcs[i-1][j]:
			find(res,i-1,j,k)
			
		elif lcs[i][j] == lcs[i][j-1]:
			find(res,i,j-1,k)
			
		else:
			find(res,i-1,j-1,k)
			
	find(res,m,n,0)
	return res
					
def main():
	a = "ABCBDAB"
	b = "BDCABA"
	
	# 此处输出lcs表格
	c = ""
	lcs = LCS(a,b)
	for ch in b:
		c += '  ' + ch
	print(c)
	for i in range(1,len(lcs)):
		print(a[i-1],lcs[i][1:])
	
	print("Maximum length: {}".format(lcs[len(a)][len(b)]))
	lcs = LCS(a,b)
	res = FindLCS(lcs,a,b)
	for str in res:
		print(str)
	
if __name__ == "__main__":
	main()