# 0-1 Knapsack Problem
# L[w][i] denotes the largest value we can get when we have weight limit as w, and
# items[0:i] to choose from.

def knapsack(values,weights,weight_limit):
	L = [[0 for _ in range(len(values)+1)] for _ in range(weight_limit+1)]
	for w in range(1,len(L)):
		for i in range(1,len(L[0])):
			if w < weights[i-1]:
				L[w][i] = L[w][i-1]
			else:
				L[w][i] = max(L[w-weights[i-1]][i-1]+values[i-1],
						  L[w][i-1])
	return L[weight_limit][len(values)]
	
def main():
	v = [20,5,10,40,15,25]
	w = [1,2,3,8,7,4]
	w_lim = 10
	res = knapsack(v,w,w_lim)
	print("knapsack value is {}".format(res))
	
if __name__ == "__main__":
	main()