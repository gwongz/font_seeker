import os
import re
import numpy as np 
import cProfile 
from sys import argv
from PIL import Image, ImageOps
import SimpleCV as cv

import model 
from seed import load_user_image, clear_user



"""Identifies letter of alphabet for each segment stored in 'user' directory and then matches to font"""

def add_user_image(directory):

	# clear db before storing what's been added to user directory	
	session = model.session
	clear_user(session)

	segments = os.listdir(directory)
	if '.DS_Store' in segments:
			segments.remove('.DS_Store')

	for imgfile in segments:
		# adds each segment to database as User_Image object 
		img_location = os.path.abspath(os.path.join(directory, imgfile))
		file_url = os.path.join(directory, imgfile)
		name = str(file_url)

		img = cv.Image(img_location)
		blobs = img.binarize().findBlobs()
		if blobs != None:
			bounds = blobs[-1].boundingBox()
			crop = img.crop(bounds).save(name)

		load_user_image(session, img_location, file_url) # location is abs path, file_url is relative path, fcn in seed.py 


def get_letter(user_dir, ocr_dir):


	segments = os.listdir(user_dir)
	if '.DS_Store' in segments:
		segments.remove('.DS_Store')

	sorted_segments = sorted_nicely(segments)


	ocr_alphabet = []
	for dirpath, dirnames, fnames in os.walk(ocr_dir):
	    	for f in fnames:
	       		if f.endswith('.png'):
	       			ocr_alphabet.append(f)

	return ocr_alphabet, sorted_segments




def find_font(ocr_alphabet, sorted_segments):

	
	font_table = {}

	for img in sorted_segments:
		directory = 'user_image'
		img_url = os.path.abspath(os.path.join(directory, img))	
		
		user_img = Image.open(img_url)
		user_width = user_img.size[0]
		user_height = user_img.size[1]

		ocr_xor = 100
		position_of_alphabet = 0
		
		for count in range(52):
			
			
			if count >= 26:
				ocr_directory = 'training_alphabet/Arial/upper'
			else:
				ocr_directory = 'training_alphabet/Arial/lower'

			ocr_letter_url = os.path.abspath(os.path.join(ocr_directory, ocr_alphabet[count]))
			print ocr_letter_url, count 

			ocr_letter = Image.open(ocr_letter_url)
			ocr_letter_width = ocr_letter.size[0]
			ocr_letter_height = ocr_letter.size[1]

			if user_width > ocr_letter_width:
				resized_user = resize_to_smaller(user_img, ocr_letter_width, ocr_letter_height)
				print "Resizing user image down to template size"
				diff = difference_of_images(resized_user, ocr_letter)

			else:
				resized_ocr = resize_to_smaller(ocr_letter, user_width, user_height)
				print "Resizing template down to user image size"
				diff = difference_of_images(resized_ocr, user_img)

			print "img_url", img_url
			print "ocr_letter_url", ocr_letter_url
			print "ocr_xor", diff 


			if diff < ocr_xor:
				ocr_xor = diff 
				position_of_alphabet = count 
				# if position is 4, that is for 'e'

			if position_of_alphabet >= 26:
				value = position_of_alphabet + 39

			else:
				value = position_of_alphabet + 97
			
			print position_of_alphabet, ocr_xor, value 
			# begin font comparisons here 

			print "Value", value 
			fonts = query_fonts(value)

			for font in fonts:
				print font 

		break

				

		
		
	return font_table		
			

	
def query_fonts(value):
	fonts = model.session.query(model.Letter.file_url).filter(model.Letter.value == value).all()
	return fonts 









def resize_to_smaller(img, new_width, new_height): # passed in as PIL imgs

	resized_img = ImageOps.fit(img, (new_width, new_height), Image.ANTIALIAS, 0, (0.5, 0.5))
	return resized_img # resized down to new width


# only works when images are identically sized 
def difference_of_images(user_img, template_img): # passed in as PIL imgs

	# loads pixel values into array 
	pixel_user = np.asarray(user_img).flatten()
	pixel_template = np.asarray(template_img).flatten()

	# performs xor match 
	difference = [i^j for i,j in zip(pixel_user, pixel_template)]	
	difference2 = [i^j for i,j in zip(pixel_template, pixel_user)]

	# however many times 255 appears in the list
	diff = difference.count(255)
	diff2 = difference2.count(255)

	total_diff = float(diff) + float(diff2)
	percent_of_diff = total_diff/float(len(pixel_user)+len(pixel_template))

	print "Percentage of difference between the two images:", percent_of_diff*100
	return percent_of_diff
	# 1 means complete difference; 0 means complete same


def sorted_nicely(list):
    """ Sorts the given iterable in the way that is expected"""
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(list, key = alphanum_key)


def main():

	user_dir = 'user_image'  
	# add_user_image(user_dir) # commits user images to database, run 
	ocr_dir = 'training_alphabet/Arial'

	letter = get_letter(user_dir, ocr_dir)

	ocr_alphabet = letter[0]
	sorted_segments = letter[1]


	print "sorted_segments", sorted_segments
	print "OCR alphabet", ocr_alphabet

	find_font(ocr_alphabet, sorted_segments)

	




if __name__ == "__main__":
	main()

