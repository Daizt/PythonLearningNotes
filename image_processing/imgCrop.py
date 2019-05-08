import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from imgRead import imgRead
import os,argparse,linecache

def main():
	parser = argparse.ArgumentParser(description="This program takes in path of original images (p0) and crops them into 200*200 images containing ellipse on the center, then saves cropped images in given directory (p1).\n")
	
	parser.add_argument('-p0', '--path0', help="Path of original images.")
	parser.add_argument('-p1', '--path1', help="Path of cropped images to be saved.(DEFAULT: cropped_images)", default='cropped_images')
	parser.add_argument('-f', '--filename', help="Filename of an original image on current directory.")
	
	args = parser.parse_args()

	currentDir = os.path.split(os.path.abspath(__file__))[0]
	destDir = os.path.join(currentDir, args.path1)
	try:
		os.mkdir(destDir)
		print("Directory made!")
	except:
		print("Directory already exists!")
	
	if args.path0:
		imageDir = os.path.join(currentDir, args.path0)
		imagePaths = [os.path.join(imageDir, x) for x in os.listdir(imageDir) if os.path.splitext(x)[1] == '.tiff']
		# read images in dataPaths and choose one channel of each image
		imgs = imgRead(*imagePaths, if_show=False)
		# choose one channel 
		imgs = [img[:,:,0] if len(img.shape)==3 else img for img in imgs]

	# we may need different half sizes to find the right area when exposure time is large.
		for i in range(len(imgs)):
			img_cropped = imageCrop(imgs[i], half_size = 500)
			img_cropped = imageCrop(img_cropped, half_size = 300)
			img_cropped = imageCrop(img_cropped, half_size = 100)
			
			# save cropped images
			filename = os.path.split(imagePaths[i])[1].split('.')[0] + '_cropped.tiff'
			# we use cmap 'gray' to save gray-scale images
			plt.imsave(os.path.join(currentDir, args.path1, filename), img_cropped, cmap='gray')
			# print max error between original images and saved images
			img_saved = imgRead(os.path.join(currentDir, args.path1, filename),if_show=False)[0][:,:,0]
			print("Max error between original array and saved image: ", np.max(np.abs(img_saved-img_cropped)))
		print("Images cropping finished!")
			
	if args.filename:
		imagePath = os.path.join(currentDir, args.filename)
		# read images in dataPaths and choose one channel of each image
		img = imgRead(imagePath, if_show=False)[0]
		# choose one channel
		if len(img.shape) == 3:
			img = img[:,:,0]

	# we may need different half sizes to find the right area when exposure time is large.
		img_cropped = imageCrop(img, half_size = 500)
		img_cropped = imageCrop(img_cropped, half_size = 300)
		img_cropped = imageCrop(img_cropped, half_size = 100)
		
		# save cropped images
		filename = args.filename.split('.')[0] + '_cropped.tiff'
		# we use cmap 'gray' to save gray-scale images
		plt.imsave(os.path.join(currentDir, filename), img_cropped, cmap='gray')
		# print max error between original images and saved images
		img_saved = imgRead(os.path.join(currentDir, filename),if_show=False)[0][:,:,0]
		print("Max error between original array and saved image: ", np.max(np.abs(img_saved-img_cropped)))
		
		print("Image cropping finished!")
	
	if args.filename==None and args.path0==None:
		print("No image cropped!")

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