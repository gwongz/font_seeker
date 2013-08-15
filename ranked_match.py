import os
import re
import numpy as np
from collections import OrderedDict

from PIL import Image, ImageOps
import SimpleCV as cv

import model 
from seed import load_user_image, clear_user
from process_images import crop_at_bounds, make_constrained



"""Runs xor against user segments and each letter of alphabet and then matches each identified letter to font"""

def process_user_image(directory):

	crop_at_bounds(directory)
	make_constrained(directory)

	segments = os.listdir(directory)
	if '.DS_Store' in segments:
		segments.remove('.DS_Store')

	session = model.session
	clear_user(session)
	
	for imgfile in segments:
		location = os.path.abspath(os.path.join(directory, imgfile))
		file_url = os.path.join(directory, imgfile)
		name = str(file_url)
		load_user_image(session, location, file_url)


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

	print "These are the user segments. They should be in alphanumeric order: ", segments
	print "These are the templates. They should be in alphabetic order: ", ocr_alphabet


	for imgfile in segments:

		user_url = os.path.abspath(os.path.join(user_dir, imgfile))	
		# user_img = img_url # 
		# relative = user_img.split('/')[-2:]
		# relative_url = os.path.join(relative[0], relative[1])
		
		count = 0 
		for letter in ocr_alphabet:

			if count > 26:
				letter_url = os.path.abspath(os.path.join(ocr_dir+'/upper', letter))
			else:
				letter_url = os.path.abspath(os.path.join(ocr_dir+'/lower', letter))
			
			print "OCR template url: ", letter_url
			print "OCR template letter", letter 

			

			# user_black_pixels_tuple = model.session.query(model.User_Image.black_pixels).filter(model.User_Image.file_url==relative_url)
			xor_of_images = difference_of_images(user_url, letter_url)
			print "This is xor_of_images", xor_of_images

			if img_url not in ocr_dict.keys():
				ocr_dict.setdefault(img_url, [xor_of_images])
			
			else:
				ocr_dict[img_url].append(xor_of_images)				
				
			count +=1
		
		# limits number of samples 
		if len(ocr_dict.keys()) > 10:
			break

	return ocr_dict # a dictionary with imgname as key and 52 percentages 

# only works when images are identically sized 
def difference_of_images(user_img, template_img): # passed in as SimpleCV images

	user = cv.Image(user_img).binarize()
	user_matrix = user.getNumpy().flatten()

	template = cv.Image(template_img).binarize()
	template_matrix = template.getNumpy().flatten()

	# print "User matrix", user_matrix
	# print 'Template matrix', template_matrix

	# performs xor match 
	difference = [i^j for i,j in zip(user_matrix, template_matrix)]	
	difference2 = [i^j for i,j in zip(template_matrix, user_matrix)]
	# print "xor of difference1", difference
	# print "xor of difference2", difference2

	# # however many times the xor returns True
	diff = difference.count(255)
	# print "Count of difference in pixel", diff

	diff2 = difference2.count(255)
	# print "Count of difference in pixel", diff2

	total_diff = diff + diff2
	xor_value = total_diff/float(len(user_matrix)+len(template_matrix))

	print "Percentage of difference between the two images:", xor_value*100
	return round(xor_value, 4)
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
	best_ocr_matches = {}
	letters = []
	user_urls = []
	
	# throws out bad ocr matches 
	for key, value in ocr_match_dict.iteritems():
		if value[0] > 0.2:
			continue
		best_ocr_matches[key] = value

	for key, value in best_ocr_matches.items():
		user_urls.append(key)
		letters.append(ord(value[2]))

	# sorts dictionary by lowest value of xor difference
	# sorted_ocr = OrderedDict(sorted(ocr_match_dict.items(), key=lambda t: t[1][0]))
	
	print "\n\n\n\nThis is the best_ocr_matches.items()", best_ocr_matches.items()
	print "These are the letter values", letters
	print "These are the user urls: ", user_urls
	return letters, user_urls, best_ocr_matches


def match_font(letters, user_urls):

	letters_to_skip = [105, 108, 73, 76]
	font_table = {}
	
	n=0
	while n < len(letters):
		# print "This is n at the top: ", n 
		user_img = user_urls[n]
		

		relative = user_img.split('/')[-2:]
		relative_url = os.path.join(relative[0], relative[1])
		print "This is relative_url", relative_url

		value = int(letters[n])
		print "This is the value to be looked up", value
		print "This is the letter to be looked up"

		user_black_pixels_tuple = model.session.query(model.User_Image.black_pixels).filter(model.User_Image.file_url==relative_url)	
		# print "This is userblack pixels tuple", user_black_pixels_tuple 
		user_black_pixels = user_black_pixels_tuple[0][0]
		print "This is the number of black pixels in user image:", user_black_pixels

		font_objects = model.session.query(model.Letter.file_url).filter(model.Letter.value == value).all()
		# print "This is the result of the fonts query", font_objects
		# print "This is the length of font_objects", len(font_objects)

		for i in range (len(font_objects)):
			print "This is i at the top", i

			if value in letters_to_skip:
			# if value == 108 or value == 105 or value == 73 or value == 76:
					print "I'm skipping a letter here: \n\n\n\n\n\n\n"
					continue

			font_location = str(font_objects[i][0])
			print "This is the font location", font_location
		
			font_black_pixels_tuple = model.session.query(model.Letter.black_pixels).filter(model.Letter.file_url == font_location)
			font_black_pixels = font_black_pixels_tuple[0][0]

			# within 5 percent margin
			black_pixels_min = user_black_pixels - 40 
			black_pixels_max = user_black_pixels + 40 

			# only xor if value of black pixels within range 
			if font_black_pixels > black_pixels_min and font_black_pixels < black_pixels_max:
			
				font_img = font_location
				font_xor = difference_of_images(user_img, font_img)
				print "The black pixels condition was met"
				print "This is the font xor", font_xor
				print "This is the user img being compared", user_img
				print "This is the font img being compared", font_img
				print "This is the letter being checked", chr(value)
				# font_aspect_ratio = model.session.query(model.Letter.aspect_ratio).filter(model.Letter.file_url==font_location)
				# print "This is the aspect ratio", font_aspect_ratio


				if font_xor <= 0.10:
					font_name = model.session.query(model.Letter.font_name).filter(model.Letter.file_url==font_location).one()
					# print "This is the fontname: ", font_name
					if font_name not in font_table.keys():
						font_table.setdefault(font_name, [font_xor])
					else:
						font_table[font_name].append(font_xor)

		n+=1
		# if len (font_table.keys()) > 5:
		# 	print "This is the length of the font table keys: ", len(font_table.keys())
		# 	break


		# if any of the items in font table has a value that exceeds 5: break 	
		# print 'This is n at the bottom: ', n 

	print "This is the length of the font table", len(font_table.items())
	return font_table


def rank_fonts(font_table, best_ocr_matches):

	print "This is the font table before ranking"
	for key, value in font_table.items():
		print key, value, '\n'

	# lowest difference by average:
	print "These are the results by lowest average of list of differences"
	lowest_average = OrderedDict(sorted(font_table.items(), key=lambda t: np.mean(t[1])))
	averageitems = lowest_average.items()

	# font table sorted by length of values list 
	# frequency = OrderedDict(sorted(font_table.items(), key=lambda t: len(t[1])))
	# highest_frequency = frequency.items()
	# highest_frequency.reverse() 
	# print "This is the font table sorted by most matches \n\n\n\n" 

	print "\n\n\n\n\n\n\n\n\n\n\n"
	print "Making some decisions now:"

	if len(font_table.items()) == 1:
		print "Match found! This is the closest match found: ", str(font_table.keys())

	if len(font_table.items()) > 1 and len(font_table.items()) < 4:
		# return top match 
		print "Match found! This is the closest match found: ", averageitems[0][0]

	if len(font_table.items()) >= 4:
		# if there are several matches	
		print "Match found: This is the closest match found: ", averageitems[0][0]
		
		averageitems.pop(0)
		while averageitems [0][1] <= .05:
			print "These were also close matches: ", averageitems[0][0]



def sorted_nicely(list):
    """ Sorts the given iterable in the way that is expected"""
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(list, key = alphanum_key)


def main():
	# commits user images to database
	# process_user_image('user_image')  
	user_dir = 'user_image'
	ocr_dir = 'ocr_alphabet/Arial'

	ocr_data = get_letter(user_dir, ocr_dir)
	# # returns dictionary that has as values: list of ALL xor matches per segment for lowercase
	print "This is the ocr_data", ocr_data.items()


	ocr_match_dict = identify_letter(ocr_data)
	print "This is the ocr_match_dict", ocr_match_dict.items()
	# returns dictionary that has as values: list of smallest xor difference 
	# value, idx position in img_data list, letter_of_alphabet (idx + 97 or idx + 65) 


	# cut run time by only appending good matches to letter to process list	
	letters_to_process = get_letters_to_process(user_dir, ocr_match_dict)
	letters = letters_to_process [0]
	user_urls = letters_to_process[1]
	best_ocr_matches = letters_to_process[2]


	font_table = match_font(letters, user_urls)
	result = rank_fonts(font_table, best_ocr_matches)
	print result 
	# return result 

if __name__ == "__main__":
	main()

	
	
