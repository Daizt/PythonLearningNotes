import torch 
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt

class K_means(nn.Module):
	def __init__(self, k):
		super().__init__()
		self.k = k

	def forward(self, Data, threshold=1):
		means = torch.randn(self.k, Data.shape[1])
		means_new = means.clone()
		delta = threshold + 1
		labels = torch.zeros(Data.shape[0], 1, dtype=torch.int32)
		while delta > threshold:
			for i in range(Data.shape[0]):
				labels[i] = torch.argmin(torch.sum((means - Data[i,:])**2, dim=1))
			
			for i in set(labels.view(-1).numpy()):
				num = torch.sum(labels.eq(i)).item()
				means_new[i] = torch.sum(torch.where(labels==i, Data, torch.zeros_like(Data)), dim=0)/num
			delta = torch.max(torch.sum((means - means_new)**2, dim=1)).item()
			means = means_new.clone()

		return means

def main():
	Data1 = 0.5*torch.randn(60,2)
	Data2 = torch.randn(60,2) + torch.tensor([[5,3]], dtype=torch.float32)
	Data3 = 1.2*torch.randn(60,2) + torch.tensor([[9,-5]], dtype=torch.float32)

	Data = torch.cat((Data1, Data2, Data3), dim=0)
	model = K_means(3)
	means = model(Data)

	fig, axs = plt.subplots()
	axs.scatter(Data1.numpy()[:,0], Data1.numpy()[:,1], label = '1')
	axs.scatter(Data2.numpy()[:,0], Data2.numpy()[:,1], label = '2')
	axs.scatter(Data3.numpy()[:,0], Data3.numpy()[:,1], label = '3')
	axs.plot(means.numpy()[:,0], means.numpy()[:,1], 'k^', markersize=10)
	axs.legend()
	plt.show()

if __name__ == '__main__':
	main()
