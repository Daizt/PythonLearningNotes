import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import matplotlib.style as mpstyle
from imgRead import imgRead
import os,argparse

def main():
	parser = argparse.ArgumentParser(description = "This program completes following jobs:\n1.Read cropped images that contain ellipse light spot.\n2.Perform PCA on cropped images and find the principle directions.\n3.Calculate length ratio of major aixs of each ellipse in the cropped images.\n")							
	parser.add_argument('-p', '--path', help="The path of cropped images.")
	parser.add_argument('-l', '--luminosity', help="Luminosity threshold. (DEFAULT: 250)", default=250, type=int)
	parser.add_argument('--show', action='store_true', help="Show flag to determine whether to show PCA result.")
	args = parser.parse_args()
	
	
	currentPath = os.path.dirname(os.path.abspath(__file__))
	imagePath = os.path.join(currentPath, args.path)
	imagePaths = [os.path.join(imagePath, x) for x in os.listdir(imagePath) if os.path.splitext(x)[1]=='.tiff']
	
	# read cropped images
	imgs = imgRead(*imagePaths, if_show=False)
	# choose one channel of each image
	imgs = [img[:,:,0] if len(img.shape)==3 else img for img in imgs]

	
	# images analysing
	ratios = np.array([imgAnalyse(img, luminosity=args.luminosity) for img in imgs])
	# show one of the PCA results
	if args.show:
		idx = np.random.choice(len(imgs))
		imgAnalyse(imgs[idx], if_show=True)
	
	# show results 
	fig, ax = plt.subplots()
	ax.plot(ratios, 'bx-', linewidth=1.2)
	ax.set_title('Variance Ratios of different images')
	ax.set_xlabel('The Number of Image')
	ax.set_ylabel('Ratios')
	ax.grid(True)
	plt.savefig('result')
	plt.show()
	
	# write results to file
	filePath = os.path.join(currentPath, 'ratios.txt')
	with open(filePath, 'w') as fp:
		for x in ratios:
			fp.write(str(x)+'\n')
	print("Results saved!")


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
	
	
	# sort all x and y, so we can get variance ratio
	X_sorted = np.sort(X_proj, axis=1)
	# how many points we use to compute lengths of major axis
	point_num = int(len(X_sorted[0])*0.01)
	if point_num < 10:
		point_num = 10
	a = np.sum(np.abs(X_sorted[0][0:point_num])+np.abs(X_sorted[0][-1-point_num:-1]))/(2*point_num)
	b = np.sum(np.abs(X_sorted[1][0:point_num])+np.abs(X_sorted[1][-1-point_num:-1]))/(2*point_num)
	variance_ratio = a/b
	
	if if_show:
		print("Points selected/total: {}/{}".format(point_num, len(X_sorted[0])))
		# show the priciple directions
		fig, ax = plt.subplots()
		ax.imshow(img, cmap='gray')
		# ax.arrow(100, 100, eigVec.T[0][0]*30, eigVec.T[0][1]*30, head_width=4, head_length=4, fc='r', ec='r')
		# ax.arrow(100, 100, eigVec.T[1][0]*30, eigVec.T[1][1]*30, head_width=4, head_length=4, fc='r', ec='r')
		ax.arrow(100, 100, U.T[0][0]*40, U.T[0][1]*40, head_width=4, head_length=4, fc='r', ec='r')
		ax.arrow(100, 100, U.T[1][0]*20, U.T[1][1]*20, head_width=4, head_length=4, fc='deepskyblue', ec='deepskyblue')


		fig2, ax2 = plt.subplots()
		ax2.plot(X_proj[0], X_proj[1], 'bx', markersize=2.5)
		ax2.plot([-a, a], [0, 0], 'r--', linewidth=1.5)
		ax2.plot([0, 0], [-b, b], 'r--', linewidth=1.5)
		ax2.axis('equal')
		#ax2.axis([-30,30,-40,40])
		plt.show()

	return variance_ratio
	
	
if __name__ == "__main__":
	main()