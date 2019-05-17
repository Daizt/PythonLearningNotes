import imageio,argparse,time,os

def main():
	parser = argparse.ArgumentParser(description="This program takes and saves screenshots for a given duration.")
	parser.add_argument('-d', '--duration', type=int, help="How long you want to keep taking screenshot.(Unit: second)")
	parser.add_argument('-i', '--interval', type=float, help="Interval.(Unit: second)", default=0.05)
	args = parser.parse_args()
	
	currentPath = os.path.split(os.path.abspath(__file__))[0]
	
	for i in range(3,0,-1):
		print("{}".format(i))
		time.sleep(1)
	print("Action!")

	t = 0
	ith = 0
	while True:
		# take & save a screenshot
		im_screen = imageio.imread('<screen>')
		imageio.imwrite(os.path.join(currentPath, 'raw_images', '{}.jpg'.format(ith)), im_screen)
		time.sleep(args.interval)
		t += args.interval
		ith += 1
		if t > args.duration:
			print("Done!")
			break
	
if __name__ == "__main__":
	main()