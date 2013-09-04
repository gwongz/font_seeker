import os
import re
import numpy as np
from shutil import rmtree 
from collections import OrderedDict

from PIL import Image, ImageOps
import SimpleCV as cv

import model 
from seed import load_user_image, clear_user
from process_images import crop_at_bounds, make_constrained


""" Makes xor comparison against user segments and OCR alphabet and compares to font template """

def check_for_segments(directory):
	segments = os.listdir(directory)
	if '.DS_Store' in segments:
		segments.remove('.DS_Store')
	return segments

def clear_segments(directory):
	if os.path.exists('user_image'):
		rmtree('user_image')
	os.mkdir('user_image')

def process_user_image(directory, segments):
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

	ocr_alphabet = []
	for dirpath, dirnames, fnames in os.walk(ocr_dir):
	    	for f in fnames:
	       		if f.endswith('.png'):
	       			ocr_alphabet.append(f)

	for imgfile in segments:
		user_url = os.path.abspath(os.path.join(user_dir, imgfile))	
		user_img = user_url 
		count = 0 

		for letter in ocr_alphabet:
			if count > 26:
				letter_url = os.path.abspath(os.path.join(ocr_dir+'/upper', letter))
			else:
				letter_url = os.path.abspath(os.path.join(ocr_dir+'/lower', letter))
			
			xor_of_images = difference_of_images(user_url, letter_url)
			print "Xor value against OCR template", xor_of_images

			if user_url not in ocr_dict.keys():
				ocr_dict.setdefault(user_url, [xor_of_images])			
			else:
				ocr_dict[user_url].append(xor_of_images)							
			count += 1
	
		# limits number of samples 
		if len(ocr_dict.keys()) > 10:
			break
	# dictionary with imgname as key and list of 52 diff values 
	return ocr_dict 


def difference_of_images(user_img, template_img): 

	user = cv.Image(user_img).binarize()
	user_matrix = user.getNumpy().flatten()

	template = cv.Image(template_img).binarize()
	template_matrix = template.getNumpy().flatten()

	# performs xor match 
	difference = [i^j for i,j in zip(user_matrix, template_matrix)]	
	# however many times xor returns True
	diff = difference.count(255)
	xor_value = diff/float(len(user_matrix))
	# 1 means complete difference
	return round(xor_value, 4)
	
def identify_letter(ocr_data):
	ocr_match_dict = {}
	for key in ocr_data.iterkeys():
		min_value = min(ocr_data[key]) # finds lowest diff value from list 
		idx_pos = ocr_data[key].index(min_value)		
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
	return letters, user_urls, best_ocr_matches


def match_font(letters, user_urls):

	letters_to_skip = [105, 108, 73, 76]
	font_table = {}
	
	n=0
	while n < len(letters):
		user_img = user_urls[n]		
		relative = user_img.split('/')[-2:]
		relative_url = os.path.join(relative[0], relative[1])
		value = int(letters[n])

		user_black_pixels_tuple = model.session.query(model.User_Image.black_pixels).filter(model.User_Image.file_url==relative_url)	
		user_black_pixels = user_black_pixels_tuple[0][0]
		font_objects = model.session.query(model.Letter.file_url).filter(model.Letter.value == value).all()
	
		for i in range (len(font_objects)):
			if value in letters_to_skip:
				continue
			font_location = str(font_objects[i][0])		
			font_black_pixels_tuple = model.session.query(model.Letter.black_pixels).filter(model.Letter.file_url == font_location)
			font_black_pixels = font_black_pixels_tuple[0][0]

			black_pixels_min = user_black_pixels - 40 
			black_pixels_max = user_black_pixels + 40 
			# only xor if value of black pixels within range 
			if font_black_pixels > black_pixels_min and font_black_pixels < black_pixels_max:		
				font_img = font_location
				font_xor = difference_of_images(user_img, font_img)
				print "The black pixels condition was met"
				print "Font xor", font_xor
	
				if font_xor <= 0.10:
					font_name = model.session.query(model.Letter.font_name).filter(model.Letter.file_url==font_location).one()
					if font_name not in font_table.keys():
						font_table.setdefault(font_name, [font_xor])
					else:
						font_table[font_name].append(font_xor)
		n+=1

	return font_table


def rank_fonts(font_table, best_ocr_matches):

	print "This is the font table before ranking"
	for key, value in font_table.items():
		print key, value, '\n'

	lowest_average = OrderedDict(sorted(font_table.items(), key=lambda t: np.mean(t[1])))
	averageitems = lowest_average.items()
	returned_matches = []
	print "\n Making some decisions now:"

	if len(font_table.items()) == 1:
		returned_matches.append(font_table.items())

	if len(font_table.items()) > 1:
		returned_matches.append(averageitems[0])
		
	print "This is the closest match: ", returned_matches
	return returned_matches

def main():
	user_dir = 'user_image'
	ocr_dir = 'ocr_alphabet/Arial'
	segments = check_for_segments(user_dir)

	if segments == [] or len(segments) <= 1:
		result = []
	# commits user images to database
	else:
		process_user_image(user_dir, segments)  
		# returns dictionary that has as values: list of ALL xor matches per segment for lowercase
		ocr_data = get_letter(user_dir, ocr_dir)
		# returns dictionary that has as values: list of smallest xor difference 
		ocr_match_dict = identify_letter(ocr_data)
		# cut run time by only appending good matches to letter to process list	
		letters_to_process = get_letters_to_process(user_dir, ocr_match_dict)
		letters = letters_to_process [0]
		user_urls = letters_to_process[1]
		best_ocr_matches = letters_to_process[2]
		font_table = match_font(letters, user_urls)
		result = rank_fonts(font_table, best_ocr_matches)

	clear_segments(user_dir)
	return result

if __name__ == "__main__":
	main()

	
	
