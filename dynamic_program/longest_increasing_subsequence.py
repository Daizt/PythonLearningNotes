# 计算最长递增子列
# L[i]的值表示在原数列a[0:n]中以a[i]结尾的最长递增子列的长度
# L_str[i]保存了在原数列a[0:n]中以a[i]结尾的最长递增子列
def LIS(a):
	L = [1 for _ in range(len(a))]
	L_str = [[a[0]]]
	for i in range(1,len(a)):
		L_str.append([])
		for j in range(i):
			if a[j] < a[i] and L[j] >= L[i]:
				L[i] = L[j] + 1
				L_str[i] = L_str[j][:] # 此处注意！要复制而不是共用！
				L_str[i].append(a[i])
	return L,L_str

def main():
	a = [0,8,4,12,2,10,6,14,1,9,5,13,3,11,7,15]
	L,L_str = LIS(a)
	print(L)
	max_length = max(L)
	max_index = [i for i,j in enumerate(L) if j == max_length]
	print([L_str[i] for i in max_index])
	
	# max_index = L.index(max(L)) # 这种方式只能返回第一个最大值的索引
	# print(L_str[max_index])

if __name__ == "__main__":
	main()