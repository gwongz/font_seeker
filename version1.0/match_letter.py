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

	ocr_dict = {}
	segments = os.listdir(user_dir)
	if '.DS_Store' in segments:
		segments.remove('.DS_Store')
		segments = sorted_nicely(segments)

	ocr_alphabet = []
	for dirpath, dirnames, fnames in os.walk(ocr_dir):
	    	for f in fnames:
	       		if f.endswith('.png'):
	       			ocr_alphabet.append(f)

	# print "These are the user segments. They should be in alphanumeric order: ", segments
	# print "These are the templates. They should be in alphabetic order: ", templates


	for imgfile in segments:

		img_url = os.path.abspath(os.path.join(user_dir, imgfile))	
		user_img = Image.open(img_url) # using PIL 
		# deterine whether to check upper or lower[?]

		count = 0 
		for letter in ocr_alphabet:

			if count > 26:
				letter_url = os.path.abspath(os.path.join(ocr_dir+'/upper', letter))

			else:
				letter_url = os.path.abspath(os.path.join(ocr_dir+'/lower', letter))
			
			print "OCR template url: ", letter_url
			print "OCR template letter", letter 

			letter = Image.open(letter_url)
			# print "This is the template size: ", letter.size

			if user_img.size[0] > letter.size:
				print "The characters in your image are being resampled and compared to the OCR templates" 
				# if user image is bigger, size it down to template size
				user_img_resized = resize_to_smaller(user_img, letter.size[0], letter.size[1])

				diff = difference_of_images(user_img_resized, letter)

				if user_img.filename not in ocr_dict.keys():
					ocr_dict.setdefault(user_img.filename, [diff])
				else:
					ocr_dict[user_img.filename].append(diff)				

			else:
				print "The OCR template is being resampled and compared to the characters in your image"
				letter_resized = resize_to_smaller(letter, user_img.size[0], user_img.size[1])
				# print letter_resized.size
				diff = difference_of_images(user_img, letter_resized)

				if user_img.filename not in ocr_dict.keys():
					ocr_dict.setdefault(user_img.filename, [diff])

				else:
					ocr_dict[user_img.filename].append(diff)

			count +=1
		# only continue if there is a bad match result?
	return ocr_dict # a dictionary with imgname as key and 52 percentages 




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


def identify_letter(ocr_data):

	ocr_match_dict = {}

	for key in ocr_data.iterkeys():
		min_value = min(ocr_data[key]) # finds lowest % diff from list, 0 is a perfect match 
		idx_pos = ocr_data[key].index(min_value)
		print min_value, idx_pos
		if idx_pos < 26:
			letter = chr(idx_pos + 97) # if lower 
		else:
			letter = chr(idx_pos + 39) # if upper 
		ocr_match_dict.setdefault(key, [min_value, idx_pos, letter])

	return ocr_match_dict

def get_letters_to_process(user_dir, ocr_match_dict):

	segments = os.listdir(user_dir)
	if '.DS_Store' in segments:
		segments.remove('.DS_Store')

	segments = sorted_nicely(segments)
	letters_to_process = []

	# output = ""
	for imgfile in segments:

		letter_tuple = []
		img_url = os.path.abspath(os.path.join(user_dir, imgfile))	
		letter = ocr_match_dict[img_url][2]

		letter_tuple.append(img_url)
		letter_tuple.append(letter)


		letters_to_process.append(letter_tuple)

		# letters_to_process.append(img_url)
		# letters_to_process.append(letter)
		# output += letter

	# print "It looks like your image says: %s" % (output) 
	return letters_to_process


def match_font(process_letter_list):

	letters = []
	user_urls = []

	for item in process_letter_list:
		user_urls.append(item[0])
		letters.append(item[1])

	font_table = {}
	n=0
	while n < len(letters):
		# print "This is n at the top: ", n 
		user_img = Image.open(user_urls[n])
		letter = letters[n] # gets you one letter
		value = ord(letter)
		fonts = model.session.query(model.Letter.file_url).filter(model.Letter.value == value).all()	

		font_urls = []
		for f in fonts:
			font_urls.append(str(f[0])) # creates a list of template imgs that can be iterated through
	
		for url in font_urls:
			
			file_location = url 
			font = Image.open(file_location)

			if user_img.size[0] > font.size[0]:
				# print "User_img.size is bigger than template size: ", user_img.size, template.size
				# if user image is bigger, size it down to template size
				user_img_resized = resize_to_smaller(user_img, font.size[0], font.size[1])
				diff = difference_of_images(user_img_resized, font)


			else:
				font_resized = resize_to_smaller(font, user_img.size[0], user_img.size[1])
				# print template_resized.size
				diff = difference_of_images(user_img, font_resized)


			# if diff <= 0.5:
			font_name = model.session.query(model.Letter.font_name).filter(model.Letter.file_url==file_location).one()
			# print "This is the fontname: ", font_name

			if font_name not in font_table.keys():
				font_table.setdefault(font_name, [diff])

			else:
				font_table[font_name].append(diff)

		n+=1
		# print 'This is n at the bottom: ', n 
	return font_table


def rank_fonts(font_table):
	for key, value in font_table.items():
		print "Ranking fonts...\n"
		print "Font, rate of difference:", key, value, '\n\n\n'  

	least_difference = min(font_table.iteritems(), key=lambda (k,v): np.mean(v))
	# print "This is the font with the least_difference with iteritems: ", least_difference
	font = least_difference[0][0]

	return "It looks like this is the font you're looking for: %s" % (font) 



	


def sorted_nicely(list):
    """ Sorts the given iterable in the way that is expected"""
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(list, key = alphanum_key)


def main():

	user_dir = 'user_image'  
	# add_user_image(user_dir) # commits user images to database, run 
	ocr_dir = 'training_alphabet/Arial'

	ocr_data = get_letter(user_dir, ocr_dir)
	# returns dictionary that has as values: list of ALL xor matches per segment for lowercase

	ocr_match_dict = identify_letter(ocr_data)
	# returns dictionary that has as values: list of smallest xor difference 
	# value, idx position in img_data list, letter_of_alphabet (idx + 97 or idx + 65) 

	
	letters_to_process = get_letters_to_process(user_dir, ocr_match_dict)
	# # runs ocr on user_image segments using dictionary created from find_letter_match 
	# # returns a sorted list of dictionaries [{segment: letter}]

	font_table = match_font(letters_to_process)
	
	result = rank_fonts(font_table)

	return result 

	




if __name__ == "__main__":
	main()

