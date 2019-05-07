import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import os, argparse

def main():
	parser = argparse.ArgumentParser(description="This program reads and shows an image.")
	
	parser.add_argument('--bit', choices=[8,10], help="Bit depth of given image.(DEFAULT: 8)", type=int, default=8)
	parser.add_argument('--rows', type=int, default=2048, help="Row number of given image.(DEFAULT: 2048)")
	parser.add_argument('--cols', type=int, default=2592, help="Columns number of given image.(DEFAULT: 2592)")
	parser.add_argument('img', help="Image to be read.")

	args = parser.parse_args()
	
	# get current file path
	currentPath = os.path.dirname(os.path.abspath(__file__))

	# read 8-bit images
	if args.bit == 8:
		dataPath = os.path.join(currentPath, args.img)
		img = imgRead(dataPath)[0]
	
	# read 10-bit raw image
	if args.bit == 10:
		dataPath = os.path.join(currentPath,args.img)
		img = imgReadBin(dataPath, rows=args.rows, columns=args.cols)

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