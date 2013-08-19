import os
import re
import numpy as np 
from collections import OrderedDict

from PIL import Image, ImageOps
import SimpleCV as cv

import model, process_images
from seed import load_user_image, clear_user
from process_images import crop_at_bounds, make_constrained



"""Triple nested loop - breaks when a font has been returned as a match 5 or more times"""

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
	sorted_segments = sorted_nicely(segments)

	ocr_alphabet = []
	for dirpath, dirnames, fnames in os.walk(ocr_dir):
	    	for f in fnames:
	       		if f.endswith('.png'):
	       			ocr_alphabet.append(f)

	return sorted_segments, ocr_alphabet # lists in alphanumeric order 



def find_match(user_dir, ocr_dir, segments, ocr_alphabet):
	"""Runs faster but arbitrary break points"""

	font_table = {}
	
	print "These are the segments:", segments
	print "This is the order of the ocr_alphabet: ", ocr_alphabet

	for imgfile in segments:

		img_url = os.path.abspath(os.path.join(user_dir, imgfile))	
		user_img = img_url # using SimpleCV

		relative = user_img.split('/')[-2:]
		relative_url = os.path.join(relative[0], relative[1])
		print "This is relative_url", relative_url # this is for user black pixels look up 
	
		count = 0 
		for letter in ocr_alphabet:
			print "Count at the top of the OCR alphabet loop", count 

			# if count equal to e or i or I, skip 
			if count >= 26:
				letter_url = os.path.abspath(os.path.join(ocr_dir+'/upper', letter))

			else:
				letter_url = os.path.abspath(os.path.join(ocr_dir+'/lower', letter))
			
			letter = letter_url
			ocr_xor = difference_of_images(user_img, letter)

			print "This is the difference %s between %s and %s" % (ocr_xor, img_url, letter_url)
	
			# initializes value for db lookup 		
			if count < 26:
				value = count + 97
		
			if count  >= 26:
				value = count + 39

			if ocr_xor <= 0.2:
				print "The difference was low enough to check the font"
				print "The letter value %d is being looked up for %s" % (ocr_xor, img_url)

				font_objects = model.session.query(model.Letter.file_url).filter(model.Letter.value == value).all()

				print "Now let's narrow down the font objects by number of black pixels"

				user_black_pixels_tuple = model.session.query(model.User_Image.black_pixels).filter(model.User_Image.file_url==relative_url)
		
				# print "This is userblack pixels tuple", user_black_pixels_tuple 
				user_black_pixels = user_black_pixels_tuple[0][0]
				print "This is the number of black pixels in user image:", user_black_pixels


				for i in range (len(font_objects)):
					font_location = str(font_objects[i][0])
				
					font_black_pixels_tuple = model.session.query(model.Letter.black_pixels).filter(model.Letter.file_url == font_location)
					font_black_pixels = font_black_pixels_tuple[0][0]

					black_pixels_min = user_black_pixels - 22.5 # range of 5% 
					black_pixels_max = user_black_pixels + 22.5 

					if font_black_pixels > black_pixels_min and font_black_pixels < black_pixels_max:

						font_img = font_location
						font_xor = difference_of_images(user_img, font_img)

						if font_xor < 0.10:

							print "The difference was low enough to append to the dictionary"
							print "This font location %s is a match for segment %s" % (font_location, img_url)
							
							font_name = model.session.query(model.Letter.font_name).filter(model.Letter.file_url==font_location).first()

							if font_name not in font_table.keys():
								font_table.setdefault(font_name, 0)
							else:
								font_table[font_name] += 1 

				most_matches = max(font_table.items(), key=lambda t: t[1])
				if most_matches[1] >= 3:
					break


			print "Font table before incrementing count: ", font_table.items()

				
		
					#### Find a way to return the next few cases 
			
			print "This is the length of the font table at the end of the font loop: ", len(font_table) 
			print "Count at the bottom of the ocr alphabet loop", count
			print "This is the font_table at the bottom of the loop: ", font_table.items()
			count +=1

	if len(font_table) <= 2:
		# return "I'm sorry. It doesn't look like I can find a good match for you. Can you try another image?"
		print "I'm sorry. It doesn't look like I can find a good match for you. Can you try another image?"
	return font_table

		
	# else:
	# 	print most_matches # do I need this because it should be 
	


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

	# # however many times 0 appears in the list
	diff = difference.count(255)
	# print "Count of difference in pixel", diff

	diff2 = difference2.count(255)
	# print "Count of difference in pixel", diff2

	total_diff = diff + diff2
	xor = total_diff/float(len(user_matrix)+len(template_matrix))

	print "Percentage of difference between the two images:", xor*100
	return xor


def rank_fonts(font_table):

	print "This is the font table"

	for key, value in font_table.items():
		print key, value, '\n'

	most_matches = sorted(font_table.items(), key=lambda t: t[1])
	print "\n\n\n\n\""
	print "This is the ordered dictionary:"
	for key, value in most_matches:
		print key, value



	print "\n\n\n\n\n\n\n\n\n\n\n"
	print "Making some decisions now:"

	# if len(most_matches.items()) == 1:
	# 	print "Match found! This is the closest match found: ", str(font_table.keys())

	# if len(font_table.items()) > 1 and len(font_table.items()) < 4:
	# 	# return top match 
	# 	print "Match found! This is the closest match found: ", averageitems[0][0]

	# if len(font_table.items()) >= 4:
	# 	# if there are several matches	
	# 	print "Match found: This is the closest match found: ", averageitems[0][0]
		
	# 	averageitems.pop(0)
	# 	while averageitems [0][1] <= .05:
	# 		print "These were also close matches: ", averageitems[0][0]




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

	font_table = find_match(user_dir='user_image', ocr_dir='ocr_alphabet/Arial', segments=segments, ocr_alphabet=ocr_alphabet)
	results = rank_fonts(font_table)

	print results 


if __name__ == "__main__":
	main()

