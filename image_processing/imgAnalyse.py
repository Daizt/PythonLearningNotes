import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from imgRead import imgRead
import os

def main():
	# get paths
	files = ["250us_1_cropped.tiff",
			"250us_2_cropped.tiff",
			"250us_3_cropped.tiff",
			"500us_1_cropped.tiff",
			"500us_2_cropped.tiff",
			"500us_3_cropped.tiff",
			"800us_1_cropped.tiff",
			"800us_2_cropped.tiff",
			"800us_3_cropped.tiff"]
	files_2 = ["250us ({})_cropped.tiff".format(i) for i in range(1,11)]
	files_2 += ["500us ({})_cropped.tiff".format(i) for i in range(1,13)]
	files_2 += ["800us ({})_cropped.tiff".format(i) for i in range(1,7)]
	
	currentPath = os.path.dirname(os.path.abspath(__file__))
	dataPaths = [os.path.join(currentPath, 'cropped_images', file) for file in files]
	dataPaths_2 = [os.path.join(currentPath, 'cropped_images', file) for file in files_2]

	# read original images
	imgs = imgRead(*dataPaths, if_show=False)
	imgs_2 = imgRead(*dataPaths_2, if_show=False)
	# choose one channel of each image
	imgs = [img[:,:,0] for img in imgs]
	imgs_2 = [img[:,:,0] for img in imgs_2]
	
	# images analysing
	Ratios = np.array([imgAnalyse(img, luminosity=240) for img in imgs])
	Ratios_2 = np.array([imgAnalyse(img, luminosity=254) for img in imgs_2])
	
	# show results of files
	# fig, ax = plt.subplots()
	# ax.plot(Ratios, 'bx-', linewidth=1.2)
	# ax.set_title('Variance Ratios of different images')
	# ax.set_xlabel('The Number of Image')
	# ax.set_ylabel('Ratios')
	# ax.axis('equal')
	# ax.grid(True)
	# plt.show()
	
	# show results of files_2
	imgAnalyse(imgs_2[5], if_show=True)
	fig, ax = plt.subplots()
	ax.plot(Ratios_2, 'bx-', linewidth=1.2)
	ax.set_title('Variance Ratios of different images')
	ax.set_xlabel('The Number of Image')
	ax.set_ylabel('Ratios')
	ax.axis('equal')
	ax.grid(True)
	plt.show()
	
		


def imgAnalyse(img, luminosity=250, if_show=False):
	'''
	This function performs PCA on certain pixels of the given image, then projects these
	pixels on their principle directions and produces variance ratio.
	
	Args:
		img: image array, type np.array([rows*columns], dtype=np.int8).
		luminosity: luminosity threshold, type int in range(0,255).
		if_show: whether to show PCA results.
		
	Returns:
		variance_ratio: variance ratio of two principle directions.
	'''
	# X contains positions of all pixels we are interested.
	X = np.argwhere(img>luminosity).T
	# we swap (x,y) to make the coordinates in accordance with those in images
	X[0], X[1] = X[1].copy(), X[0].copy()
	# make x in X has zero mean
	X -= 100

	# perform PCA, we can either use svd or eigendecomposition
	U,S,Dt = np.linalg.svd(X.dot(X.T))
	# eigVal, eigVec = np.linalg.eig(X.dot(X.T))
	
	# project all x in X to the principle directions
	X_proj = U.T.dot(X)
	
	if if_show:
		# show the priciple directions
		fig, ax = plt.subplots()
		ax.imshow(img, cmap='gray')
		# ax.arrow(100, 100, eigVec.T[0][0]*30, eigVec.T[0][1]*30, head_width=4, head_length=4, fc='r', ec='r')
		# ax.arrow(100, 100, eigVec.T[1][0]*30, eigVec.T[1][1]*30, head_width=4, head_length=4, fc='r', ec='r')
		ax.arrow(100, 100, U.T[0][0]*40, U.T[0][1]*40, head_width=4, head_length=4, fc='r', ec='r')
		ax.arrow(100, 100, U.T[1][0]*20, U.T[1][1]*20, head_width=4, head_length=4, fc='deepskyblue', ec='deepskyblue')


		fig2, ax2 = plt.subplots()
		ax2.plot(X_proj[0], X_proj[1], 'bx', markersize=2.5)
		ax2.axis('equal')
		#ax2.axis([-30,30,-40,40])
		plt.show()
	
	# sort all x and y, so we can get variance ratio
	X_sorted = np.sort(X_proj, axis=1)
	a = np.sum(np.abs(X_sorted[0][0:5])+np.abs(X_sorted[0][-6:-1]))/10
	b = np.sum(np.abs(X_sorted[1][0:5])+np.abs(X_sorted[1][-6:-1]))/10
	variance_ratio = a/b

	return variance_ratio
	
	
if __name__ == "__main__":
	main()