
import os
import re
import numpy 
from sys import argv
from bisect import bisect_left, bisect_right
# from PIL import Image, ImageChops
# from SimpleCV import Image 
from PIL import Image, ImageOps
import SimpleCV as cv
import seed
import model 


"""Identifies letter of alphabet for each segment stored in 'user' directory"""


def clear_user_image(session):
	user_img = model.session.query(model.User_Image).all()
	
	for imgfile in user_img:
		session.delete(imgfile)
		session.commit()

def add_user_image(directory):

	# clear db before storing what's been added to user directory	
	session = model.session
	clear_user_image(session)

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
		bounds = blobs[-1].boundingBox()
		
		crop = img.crop(bounds).save(name)

		seed.load_user_image(session, img_location, file_url) # location is abs path, file_url is relative path 


def run_comparisons(user_dir, templates_dir):

	match_values = {}
	segments = os.listdir(user_dir)
	if '.DS_Store' in segments:
		segments.remove('.DS_Store')

	for imgfile in segments:

		img_url = os.path.abspath(os.path.join(user_dir, imgfile))	
		user_img = Image.open(img_url) # using PIL 
		# deterine whether to check upper or lower[?]


		templates = os.listdir(templates_dir)
		if '.DS_Store' in templates:
			templates.remove('.DS_Store')
		if 'upper' in templates:
			templates.remove('upper')

		
		for templatefile in templates:		
		
			template_url = os.path.abspath(os.path.join(templates_dir, templatefile))
			print "Template url: ", template_url
			print "Templatefile", templatefile
		
			template = Image.open(template_url)
			print "This is template size: ", template.size

			if user_img.size > template.size:
				print "User_img.size is bigger than template size: ", user_img.size, template.size
				# if user image is bigger, size it down to template size
				user_img_resized = resize_to_smaller(user_img, template.size[0], template.size[1])

				diff = difference_of_images(user_img_resized, template)

				if user_img.filename not in match_values.keys():
					match_values.setdefault(user_img.filename, [diff])
				else:
					match_values[user_img.filename].append(diff)				
				
				# match_values.setdefault(user_img.filename, []).append(diff)
				# match_values[user_img.filename] = match_values.get(user_img.filename, [])
				# match_values.setdefault(user_img.filename, [diff])

			

			else:
				template_resized = resize_to_smaller(template, user_img.size[0], user_img.size[1])
				print template_resized.size


				diff = difference_of_images(user_img, template_resized)
				if user_img.filename not in match_values.keys():

					match_values.setdefault(user_img.filename, [diff])

				else:
					match_values[user_img.filename].append(diff)
				# match_values[user_img.filename] = match_values.get(user_img.filename, [])

		# run another function passing in comparison_table
		# only continue if there is a bad match result :	

		

	return match_values # a dictionary with imgname as key and 26 percentages 
	

	

def resize_to_smaller(img, new_width, new_height): # passed in as PIL Images

	# new_width = smaller_img.size[0] # will this work with PIL 
	# new_height = smaller_img.size[1]
	resized_img = ImageOps.fit(img, (new_width, new_height), Image.ANTIALIAS, 0, (0.5, 0.5))
	return resized_img # resized down to new width


# only works when images are identically sized 
def difference_of_images(user_img, template_img): # using XOR in python, passed in as PIL imgs

	# loads pixel values into array 
	pixel_user = numpy.asarray(user_img).flatten()
	pixel_template = numpy.asarray(template_img).flatten()

	# performs xor match 
	difference = [i^j for i,j in zip(pixel_user, pixel_template)]	
	difference2 = [i^j for i,j in zip(pixel_template, pixel_user)]
	
	# user_matrix = user_img.getNumpy().flatten()
	# template_matrix = template_img.getNumpy().flatten()

	# difference = [i ^ j for i, j in zip(user_matrix, template_matrix)]
	# difference2 = [i ^ j for i, j in zip(template_matrix, user_matrix)]

	# however many times 255 appears in the list - however many times 
	difference = difference.count(255)
	difference2 = difference2.count(255)

	
	percent_of_diff = difference/float(len(pixel_user))
	print "This is the percent_of_diff", percent_of_diff

	return percent_of_diff
	
	
	# total_diff = float(len(difference)) + float(len(difference2))
	# pixel_count = float(len(img1)) + float(len(img2))
	# percent_of_diff = total_diff/pixel_count
	# print percent_of_diff
	#1 means complete difference; 0 means complete same


def find_letter_match(img_data):

	letter_match_dict = {}
		
	for key in img_data.iterkeys():
		min_value = min(img_data[key]) # finds lowest % diff from list
		idx_pos = img_data[key].index(min_value)
		print min_value, idx_pos
		letter = chr(idx_pos + 97)
		letter_match_dict.setdefault(key, [min_value, idx_pos, letter])

	return letter_match_dict

def perform_ocr(user_dir, img_data, letter_match_dict):
	segments = os.listdir(user_dir)
	if '.DS_Store' in segments:
		segments.remove('.DS_Store')

	segments = sorted_nicely(segments)

	output = ""
	for imgfile in segments:

		img_url = os.path.abspath(os.path.join(user_dir, imgfile))	
		print "This is the img_url", img_url
		print "This is the imgfile", imgfile
		letter = letter_match_dict[img_url][2]
		output += letter

	print "It looks like your image says: %s" % (output) 



		

def sorted_nicely(list):
    """ Sorts the given iterable in the way that is expected.
 
    Required arguments:
    l -- The iterable to be sorted.
 
    """
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(list, key = alphanum_key)



def main():

	# directory = 'user_image'
	# add_user_image(directory) # commits user images to database
	

	img_data = run_comparisons('user_image', 'training_alphabet/Arial')

	list_of_segments = img_data.keys()

	letter_match_dict = find_letter_match(img_data)

	# print letter_match_dict.items()

	perform_ocr('user_image', img_data, letter_match_dict)
	# runs ocr on user_image segments using dictionary created from find_letter_match  

	# match = find_letter_match(img_data, list_of_segments)
	# print match 
	# letter = find_letter_match(img_data, '/Users/gwongz/src/hackbright/project/user_image/segment_0.png')
	# print letter 
	
	# for key in img_data.iterkeys():
	# 	match_list = img_data[key]
	# 	min_value = min(match_list)
	# 	idx_pos = match_list.index(min_value)
	# print "This is the key: ", key, '\n', "This is the idx posiiton:", idx_pos
	# print "This is the min_value", min_value
	# print "This is the match_list", match_list
	# mylist = sorted(match_list)
	# print "This is the sorted match list", mylist

	# identify_letter()
	# get_user_images()

if __name__ == "__main__":
	main()





