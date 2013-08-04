import numpy as np 
from sys import argv
# from PIL import Image, ImageChops
from SimpleCV import Image
import model 

"""Loads segments from get_segments and matches each segment against
letters in training alphabet to return best match"""


def load_image(img):
	img = Image(img)
	# if img.mode != 1:
	# 	img = img.convert('1')
	img = img.load()
	# loads pixel values 
	# img = img.getdata()
	# width = img.size[0]
	# height = img.size[1]
	return img

def load_training_alphabet(letter_value):

	letter = model.session.query(model.Trainer).filter(model.Trainer.value==letter_value).first()
	location = letter.file_url
	value = letter.value 

	
	return location # opens up 'A' in the training alphabet
	

	




def identify_letter(segments):
	"""Identifies what letter a segment is"""
	# < len(segments):
	# n=0
	# while n ==0: 
	match = False

	while match not True:
		img1 = Image(segments[0])
		letter_value = 65
		img2_location = load_training_alphabet(letter_value)
		img2 = Image(image2_location)
		
		width = max(img1.width, img2.width)
		height = max(img1.height, img2.height)

		# if img1 is bigger, resize it down to img2 size
		if img1.size() > img2.size():
			img = img1.resize(width, height)

		else:
			img = img2.resize(width, height)







		# if img1[1]
		# # see which one is bigger or smaller and resize 

		# difference_of_images(img1, img2)




		# don't forget to increment letter value
		# n+=1 # increments n 

def difference_of_images(img1, img2): # using XOR in python

	
	difference = [i ^ j for i, j in zip(img1, img2)]
	difference2 = [i ^ j for i, j in zip(img2, img1)]


	difference = difference.count(255)
	difference2 = difference2.count(255)

	
	percent_of_diff = difference/float(len(img1))
	return percent_of_diff
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
	
	# script, infile1, infile2 = argv
	segments = ['user_crop0.png', 'user_crop2.png']
	# load_training_alphabet(65)
	# difference_of_images(segments)

if __name__ == "__main__":
	main()





