import os
import re
import numpy as np 
import cProfile 
from sys import argv
from PIL import Image, ImageOps
import SimpleCV as cv

import model, process_images
from seed import load_user_image, clear_user
from process_images import crop_at_bounds, make_constrained



"""Identifies letter of alphabet for each segment stored in 'user' directory and then matches to font"""

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
	
	segments = os.listdir(user_dir)
	if '.DS_Store' in segments:
		segments.remove('.DS_Store')
		segments = sorted_nicely(segments)

	ocr_alphabet = []
	for dirpath, dirnames, fnames in os.walk(ocr_dir):
	    	for f in fnames:
	       		if f.endswith('.png'):
	       			ocr_alphabet.append(f)

	return segments, ocr_alphabet # lists in alphanumeric order 



def find_match(user_dir, ocr_dir, segments, ocr_alphabet):
	"""Runs faster but no good real methodology for accuracy"""

	font_table = {}
	
	print "These are the segments:", segments
	print "This is the order of the ocr_alphabet: ", ocr_alphabet

	for imgfile in segments:

		img_url = os.path.abspath(os.path.join(user_dir, imgfile))	
		user_img = Image.open(img_url).convert('1') # using PIL 
	
		count = 0 
		for letter in ocr_alphabet:
			print "Count at the top of the OCR alphabet loop", count 

			if count >= 26:
				letter_url = os.path.abspath(os.path.join(ocr_dir+'/upper', letter))

			else:
				letter_url = os.path.abspath(os.path.join(ocr_dir+'/lower', letter))
			
			letter = Image.open(letter_url).convert('1')
			diff = difference_of_images(user_img, letter)

			print "This is the difference %s between %s and %s" % (diff, img_url, letter_url)
	
			# initializes value for db lookup 		
			if count < 26:
				value = count + 97
		
			if count  >= 26:
				value = count + 39



			if diff <= 0.005:
				print "The difference was low enough to check the font"
				print "The letter value %d is being looked up for %s" % (value, img_url)

				font_objects = model.session.query(model.Letter.file_url).filter(model.Letter.value == value).all()

				for i in range (len(font_objects)):
					font_location = str(font_objects[i][0])
					font_img = Image.open(font_location).convert('1')
					font_diff = difference_of_images(user_img, font_img)

					if font_diff < 0.03:

						print "The difference was low enough to append to the dictionary"
						print "This font location %s is a match for segment %s" % (font_location, img_url)
						
						font_name = model.session.query(model.Letter.font_name).filter(model.Letter.file_url==font_location).first()

						if font_name not in font_table.keys():
							font_table.setdefault(font_name, 0)
						else:
							font_table[font_name] += 1 


			if len(font_table) > 2:
				most_matches = max(font_table.iteritems(), key=lambda (k,v): v)

				if most_matches[1] >=10:
					print "This is most matches when it's exceeded 10:", most_matches
					font = str(most_matches[0])
					
					break 

			count +=1

			print "This is the length of the font table at the end of the font loop: ", len(font_table) 
			print "Count at the bottom of the ocr alphabet loop", count
	
	print most_matches
	


# only works when images are identically sized 
def difference_of_images(user_img, template_img): # passed in as PIL imgs

	# loads pixel values into array 
	pixel_user = np.asarray(user_img).flatten()
	pixel_template = np.asarray(template_img).flatten()

	# performs xor match 
	difference = [i^j for i,j in zip(pixel_user, pixel_template)]	
	difference2 = [i^j for i,j in zip(pixel_template, pixel_user)]

	# number of times 1 (True) appears in the list --> pixels are exclusively different
	diff= difference.count(1)
	# print "This is the amount of difference: ", diff
	diff2 = difference.count(1)


	total_diff = float(diff) + float(diff2)
	percent_of_diff = total_diff/float(len(pixel_user)+len(pixel_template))

	print "Percentage of difference between the two images:", percent_of_diff*100
	return round(percent_of_diff, 4)
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


	# process_user_image(directory='user_image') # commits user image to database

	base_data = get_letter(user_dir='user_image', ocr_dir='ocr_alphabet')
	segments = base_data[0]
	ocr_alphabet = base_data[1]



	find_match(user_dir='user_image', ocr_dir='ocr_alphabet/Arial', segments=segments, ocr_alphabet=ocr_alphabet)



	
	# result = rank_fonts(font_table)

	# return result 

	




if __name__ == "__main__":
	main()

