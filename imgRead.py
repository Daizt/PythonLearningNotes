import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import os

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

def main():
	# filename1 = 'mono8.tiff'
	# filename2 = 'mono10.tiff'
	# currentPath = os.getcwd()
	# dataPath1 = os.path.join(currentPath,filename1)
	# dataPath2 = os.path.join(currentPath,filename2)

	# imgs = imgread(dataPath1,dataPath2)
	
	with open('mono10.bin','rb') as fp:
		rows, columns = 2048, 2592
		img = np.fromfile(fp, dtype=np.int16, count=-1)
		
	img.resize(rows, columns)
	plt.imshow(img)
	plt.show()
	
if __name__ == "__main__":
	main()