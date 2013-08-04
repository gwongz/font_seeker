import numpy as np 
from sys import argv
from PIL import Image, ImageChops



"""Experimenting with XOR on images"""


def load_image(img):
	img = Image.open(img)
	if img.mode != 1:
		img = img.convert('1')
	# loads pixel values 
	img = img.getdata()
	return img 


def difference_of_images(img1, img2): # using XOR in python

	
	difference = [i ^ j for i, j in zip(img1, img2)]
	difference2 = [i ^ j for i, j in zip(img2, img1)]


	difference = difference.count(255)
	difference2 = difference2.count(255)

	print difference
	print difference2
	percent_of_diff = difference/float(len(img1))
	print percent_of_diff
	#however many times 255 appears in the list
	
	# total_diff = float(len(difference)) + float(len(difference2))
	# pixel_count = float(len(img1)) + float(len(img2))
	# percent_of_diff = total_diff/pixel_count
	# print percent_of_diff
#1 means complete difference; 0 means complete same

	




# def difference_of_images(img1, img2): # need loaded pixels
# 	diff = []
# 	diff2 = []

# 	for pixel in img1:
# 		for pixel2 in img2:
# 			if pixel != pixel2:
# 				diff.append(pixel - pixel2)
# 				diff2.append(pixel2 - pixel)
# 		break
	
# 	total_diff = float(len(diff)) + float(len(diff2))
# 	pixel_count = float(len(img1)) + float(len(img2))
# 	percent_of_diff = total_diff/pixel_count
# #1 means complete difference; 0 means complete same

# 	return percent_of_diff

# img1 = load_image('rockwell_b.png')
# img2 = load_image('rockwell_a.png')
# print difference_of_images(img1, img2)



# using ImageChops instead of nested loops
# imga = Image.open('cropped_right.png')
# imgb = Image.open('cropped_left.png')
# diffa = ImageChops.difference(imga, imgb) # returns an image object
# diffa = diffa.getdata() # loads pixels of image object
# chops = []
# for pixel in diffa:
# 	if pixel != 0: # if there is any difference in the two pixels:
# 		chops.append(pixel)
# num_of_different_pixels = len(chops) 
# total_pixels = len(diffa)
# percent = num_of_different_pixels/total_pixels

# print "This is the difference obtained through ImageChops: ", percent



def main():
	
	script, infile1, infile2 = argv
	img1 = load_image(infile1)
	img2 = load_image(infile2)

	difference_of_images(img1, img2)

if__name__ == "__main__":
	main()





