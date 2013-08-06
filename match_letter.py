
import os
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


def sort_alphabet():
	alphabet = model.session.query(model.Training_Letter).all()
	alphabet_aspect_ratios = []
	for letter in alphabet:
		alphabet_aspect_ratios.append(letter.aspect_ratio)

	sorted_alphabet = sorted(alphabet_aspect_ratios)
	return sorted_alphabet

def make_alphabet_dictionary():
	
	alphabet_dict = {}
	alphabet = model.session.query(model.Training_Letter.value).all()

	for letter in alphabet:
		value = letter[0]
		alphabet_ratios = model.session.query(model.Training_Letter.aspect_ratio).filter(model.Training_Letter.value==value).all()
	
		
		for ratio in alphabet_ratios:
			alphabet_dict.setdefault(value, ratio)

	return alphabet_dict # key is letter value, value is aspect ratio 

def match_proportions(user_dir, sorted_alphabet):
 
	proportion_matches = {}

	segments = os.listdir(user_dir)
	if '.DS_Store' in segments:
		segments.remove('.DS_Store')

	# iterate through each of the segments and find best proportion matches for each segment 
	for imgfile in segments:
		img_url = os.path.abspath(os.path.join(user_dir, imgfile))
		# print "Segments imglocation: ", img_url
		img = cv.Image(img_url)
		segment_ratio = float(img.width)/float(img.height)

		closest = min(sorted_alphabet, key=lambda x:abs(x-segment_ratio))
		index_pos = sorted_alphabet.index(closest)

		# start has to be greater than 0 
		start = index_pos - 3
		if start < 0:
			start = 0
		# stop has to be within index range of alphabet list 
		stop = index_pos + 3
		if stop > len(sorted_alphabet)-1:
			stop = -1

		matches = sorted_alphabet[start:stop]
		# print "This is segment ratio up top", segment_ratio
		proportion_matches.setdefault(img.filename, matches)

	return proportion_matches # a dictionary 

def identify_letter(proportion_matches):
	# proportion matches is a dict with imgfilename as key and letters that are top matching 
	letter_proportions = {}
	for key, value in proportion_matches.items():
		name = key
		letters = []
		n=0
		while n < len(value)-1:
			aspect_ratio = value[n]
			letter_values = model.session.query(model.Training_Letter.value).filter(model.Training_Letter.aspect_ratio == aspect_ratio).first()
			letters.append(letter_values)
			n+=1
		letter_proportions.setdefault(name, letters)
	return letter_proportions	# another dictionary - these are the letters that we want to run xor on 


def run_comparisons(user_dir, templates_dir):

	comparison_table = {}
	
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

				# if user image is bigger, size it down to template size
				user_img_resized = resize_to_smaller(user_img, template.size[0], template.size[1])
				diff = difference_of_images(user_img, template)

				
				comparison_table.setdefault(user_img.filename, []).append(diff)
				# comparison_table[user_img.filename] = comparison_table.get(user_img.filename, [])
			# comparison_table.setdefault(user_img.filename, [diff])

			

			else:
				template_resized = resize_to_smaller(template, user_img.size[0], user_img.size[1])
				print template_resized.size


				diff = difference_of_images(user_img, template)
				comparison_table.setdefault(user_img.filename, []).append(diff)
				# comparison_table[user_img.filename] = comparison_table.get(user_img.filename, [])


				
			# comparison_table.setdefault(user_img.filename, [diff])

			

	return comparison_table
	

		










		




def resize_to_smaller(img, new_width, new_height): # passed in as PIL Images

	
	# new_width = smaller_img.size[0] # will this work with PIL 
	# new_height = smaller_img.size[1]

	resized_img = ImageOps.fit(img, (new_width, new_height), Image.ANTIALIAS, 0, (0.5, 0.5))

	return resized_img # resized down to new width




# only works when images are identically sized 
def difference_of_images(user_img, template_img): # using XOR in python, passed in as simplecv imgs

	pixel_user = numpy.asarray(user_img).flatten()
	pixel_template = numpy.asarray(template_img).flatten()

	difference = [i^j for i,j in zip(pixel_user, pixel_template)]	
	
	# user_matrix = user_img.getNumpy().flatten()
	# template_matrix = template_img.getNumpy().flatten()

	# difference = [i ^ j for i, j in zip(user_matrix, template_matrix)]
	# difference2 = [i ^ j for i, j in zip(template_matrix, user_matrix)]

	#however many times 255 appears in the list
	difference = difference.count(255)
	# difference2 = difference2.count(255)

	
	percent_of_diff = difference/float(len(pixel_user))
	print "This is the percent_of_diff", percent_of_diff

	return percent_of_diff
	
	
	# total_diff = float(len(difference)) + float(len(difference2))
	# pixel_count = float(len(img1)) + float(len(img2))
	# percent_of_diff = total_diff/pixel_count
	# print percent_of_diff
	#1 means complete difference; 0 means complete same

			



		





def main():
	# sorted_alphabet = sort_alphabet()
	# # directory = 'user_image'
	# # add_user_image(directory) # commits user images to database
	# p = match_proportions('user_image', sorted_alphabet) # return dictionary 
	# letters = identify_letter(p) # another dictionary

	# make_alphabet_dictionary()

	font_table = run_comparisons('user_image', 'training_alphabet/Arial')
	print font_table.items()

	# identify_letter()
	# get_user_images()

if __name__ == "__main__":
	main()





