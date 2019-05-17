import os,argparse
from PIL import Image
from PIL import ImageEnhance

def main():
	parser = argparse.ArgumentParser(description="This program crops and saves a series of images.")
	
	parser.add_argument('-p', '--path', nargs='+', help="Path of original images.")
	parser.add_argument('-r', '--rows', type=int, nargs='+', help="Row range to choose.")
	parser.add_argument('-c', '--columns', type=int, nargs='+', help="Column range to choose.")
	
	args = parser.parse_args()
	
	currentPath = os.path.split(os.path.abspath(__file__))[0]
	filePath = os.path.join(currentPath, *args.path)
	fileNames = [os.path.join(filePath, x) for x in os.listdir(filePath)]
	outputPath = os.path.join(currentPath, 'cropped_images')
	
	try:
		os.mkdir(outputPath)
		print("Directory made!")
	except:
		print("Directory already exists!")
		
		
	im = Image.open(fileNames[0])
	shape = im.size
	
	if not args.rows:
		r_1, r_2 = 0, shape[1]
	else:
		r_1, r_2  = args.rows
		
	if not args.columns:
		c_1, c_2 = 0, shape[0]
	else:
		c_1, c_2 = args.columns
	
	box = (c_1, r_1, c_2, r_2)
	size = (180, 230)

	for file in fileNames:
		outputName = os.path.split(file)[1].split('.')[0] + '_cropped.jpg'
		im = Image.open(file)
		im_cropped = im.crop(box)
		im_cropped.thumbnail(size)
		
		# Adjust image brightness
		# An enhancement factor of 0.0 gives a black image. A factor of 1.0 
		# gives the original image.
		enhancer_1 = ImageEnhance.Brightness(im_cropped)
		enhanced_1 = enhancer_1.enhance(1.5)
		
		# Adjust image color balance
		# An enhancement factor of 0.0 gives a black and white image. A factor 
		# of 1.0 gives the original image.
		enhancer_2 = ImageEnhance.Color(enhanced_1)
		enhanced_2 = enhancer_2.enhance(1.1)
		
		# Adjust image contrast
		# An enhancement factor of 0.0 gives a solid grey image. A factor of 1.0 
		# gives the original image.
		enhancer_3 = ImageEnhance.Contrast(enhanced_2)
		enhanced_3 = enhancer_3.enhance(1.1)
		
		# Adjust image sharpness
		# An enhancement factor of 0.0 gives a blurred image, a factor of 1.0 gives 
		# the original image, and a factor of 2.0 gives a sharpened image.
		enhancer_4 = ImageEnhance.Sharpness(enhanced_3)
		enhanced_4 = enhancer_4.enhance(1.3)
		
		# Save the image
		enhanced_4.save(os.path.join(outputPath, outputName))
		
	print("Done!")
	
if __name__ == "__main__":
	main()