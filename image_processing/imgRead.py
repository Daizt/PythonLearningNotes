import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import os

def main():
	# get current file path
	path = os.path.dirname(os.path.abspath(__file__))

	# read 8-bit images
	file1 = 'mono8.tiff'
	file2 = 'mono10.tiff'
	dataPath1 = os.path.join(path, 'raw_images', file1)
	dataPath2 = os.path.join(path, 'raw_images', file2)
	imgs = imgRead(dataPath1,dataPath2)
	
	# read 10-bit raw image
	file3 = 'mono10.bin'
	dataPath3 = os.path.join(path, 'raw_images', file3)
	imgs = imgReadBin(dataPath3)

def imgRead(*dataPath,if_show=True):
	imgs = []
	for path in dataPath:
		imgs.append(mpimg.imread(path))
	if if_show:
		for img in imgs:
			plt.figure()
			plt.imshow(img)
		plt.show()
	return imgs

def imgReadBin(*dataPath, rows=2048, columns=2592, if_show=True):
	imgs = []
	for path in dataPath:
		with open(path, 'rb') as fp:
			img = np.fromfile(fp, dtype=np.int16, count=-1)
			imgs.append(img.reshape(rows, columns))
	if if_show:
		for img in imgs:
			plt.figure()
			plt.imshow(img)
		plt.show()
	return imgs
	
if __name__ == "__main__":
	main()