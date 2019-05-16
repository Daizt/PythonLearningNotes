import imageio,os,argparse

def main():
	parser = argparse.ArgumentParser(description="This program reads a series of images and outputs a combined .gif file.")
	parser.add_argument('-p', '--path', nargs='+', help="Path of input images.")
	parser.add_argument('-d', '--duration', type=float, help="Duration of each frame.(DEFAULT=0.1s)", default=0.1)
	args = parser.parse_args()
	
	currentPath = os.path.split(os.path.abspath(__file__))[0]
	filePath = os.path.join(currentPath, *args.path)
	fileNames = [os.path.join(filePath, x) for x in os.listdir(filePath)]

	images = []

	for filename in fileNames:
		images.append(imageio.imread(filename))
	imageio.mimsave(os.path.join(currentPath, 'output.gif'), images, duration=args.duration)
	print("Done!")
	
if __name__ == "__main__":
	main()