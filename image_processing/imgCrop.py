import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from imgRead import imgRead
import os

def main():
	# set filenames and paths
	files = ["250us_1.tiff",
			"250us_2.tiff",
			"250us_3.tiff",
			"500us_1.tiff",
			"500us_2.tiff",
			"500us_3.tiff",
			"800us_1.tiff",
			"800us_2.tiff",
			"800us_3.tiff"]
	files_2 = ["250us ({}).tiff".format(i) for i in range(1,11)]
	files_2 += ["500us ({}).tiff".format(i) for i in range(1,13)]
	files_2 += ["800us ({}).tiff".format(i) for i in range(1,7)]
	currentPath = os.path.dirname(os.path.abspath(__file__))
	# dataPaths = [os.path.join(currentPath, 'raw_images', file) for file in files]
	dataPaths = [os.path.join(currentPath, 'raw_images', file) for file in files_2]
	
	# read images in dataPaths and choose one channel of each image
	# imgs = imgRead(*dataPaths, if_show=False)
	# imgs = [img[:,:,0] for img in imgs]
	imgs = imgRead(*dataPaths, if_show=False)
	imgs = [img[:,:,0] for img in imgs]


	# we may need different half sizes to find the right area when exposure time is large.
	for i in range(len(imgs)):
		img_cropped = imageCrop(imgs[i], half_size = 500)
		img_cropped = imageCrop(img_cropped, half_size = 300)
		img_cropped = imageCrop(img_cropped, half_size = 100)
		
		# plt.imshow(img_cropped)
		# title = os.path.basename(dataPaths[i]).strip('.tiff') + '_cropped'
		# plt.title(title)
		# #plt.colorbar()
		# plt.axis('off')
		# plt.show()
		
		# save cropped images
		filename = os.path.basename(dataPaths[i]).strip('.tiff') + '_cropped.tiff'
		# we use cmap 'gray' to save gray-scale images
		plt.imsave(os.path.join(currentPath, 'cropped_images', filename), img_cropped, cmap='gray')
		# print max error between original images and saved images
		# img_saved = imgRead(os.path.join(currentPath, 'cropped_images', filename),if_show=False)[0][:,:,0]
		# print(np.max(np.abs(img_saved-img_cropped)))
		

def imageCrop(img, luminousity = 254, half_size=100, delta=10):
	'''
	A helper function that crops original image using clusering method.
	
	Args:
		img: 8-bit image of single channel ,type np.array([height * width]).
		luminousity: luminousity threshold, type int (0~254).
		half_size: half size of the output image, type int.
		delta: threshold value of iteration,type int.
	
	Return:
		img_cropped: cropped image containing certain area.
	'''
	
	# we original image with padding which prevent invalid cropping
	img_padded = np.zeros([img.shape[0]+2*half_size, img.shape[1]+2*half_size])
	img_padded[half_size:half_size+img.shape[0], half_size:half_size+img.shape[1]] += img.copy()
	
	# initial iteration values
	# find all pixels we are interested
	X = np.argwhere(img_padded > luminousity)
	
	# find central position
	x_mean, y_mean = np.sum(X, axis=0)//X.shape[0]
	
	while True:
		# crop original image based on last central position
		img_cropped = img_padded[x_mean-half_size:x_mean+half_size, y_mean-half_size:y_mean+half_size].copy()
		
		# find relative central position of the cropped image
		X2 = np.argwhere(img_cropped > luminousity)
		x_mean2, y_mean2 = np.sum(X2, axis=0)//X2.shape[0]
		
		# compute center offset
		x_offset, y_offset = x_mean2-half_size, y_mean2-half_size
		
		# update absolute central position
		x_mean, y_mean = x_mean + x_offset, y_mean + y_offset
		
		# check if iteration converges
		if abs(x_offset) < delta and abs(y_offset) < delta:
			break	
			
	# get the cropped image based on final central position
	img_cropped = img_padded[x_mean-half_size:x_mean+half_size, y_mean-half_size:y_mean+half_size].copy()
	
	return img_cropped
	
	
if __name__ == "__main__":
	main()