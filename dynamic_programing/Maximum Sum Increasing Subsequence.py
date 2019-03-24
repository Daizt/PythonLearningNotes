# MSIS(Maximum Sum Increasing Subsequence)
# sum[i] denotes the maximum sum of an increasing subsequence that ends with a[i]
# subseq[i] memorize the MSIS that ends with a[i]

def MSIS(a):
	sum = [0 for _ in range(len(a))]
	subseq = [[]for _ in range(len(a))]
	sum[0],subseq[0] = a[0],[a[0]]
	for i in range(1,len(a)):
		for j in range(i):
			if a[j] < a[i] and sum[j] > sum[i]:
				sum[i] = sum[j]
				subseq[i] = subseq[j][:]
		sum[i] += a[i]
		subseq[i].append(a[i])
	return sum,subseq
	
def main():
	a = [8,4,12,2,10,6,14,1,9,5,13,3,11]
	sum,subseq = MSIS(a)
	max_sum = max(sum)
	max_sum_index = [i for i,j in enumerate(sum) if j == max_sum]
	print("max sum: {}".format(max_sum))
	print("MSIS: {}".format([subseq[i] for i in max_sum_index]))
			
if __name__ == "__main__":
	main()