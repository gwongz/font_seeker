
import os
from sys import argv
from bisect import bisect_left, bisect_right
# from PIL import Image, ImageChops
from SimpleCV import Image 
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

		img = Image(img_location)
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


def match_proportions(user_dir, sorted_alphabet):

	# alphabet ratios is sorted list 
	
	proportion_matches = {}

	segments = os.listdir(user_dir)
	if '.DS_Store' in segments:
		segments.remove('.DS_Store')

	print "These are the segments"	


	# iterate through each of the segments and find best proportion matches for each segment 
	for imgfile in segments:
		img_url = os.path.abspath(os.path.join(user_dir, imgfile))
		print "Segments imglocation: ", img_url
		img = Image(img_url)
		segment_ratio = float(img.width)/float(img.height)

		closest = min(sorted_alphabet, key=lambda x:abs(x-segment_ratio))
		index_pos = sorted_alphabet.index(closest)

		# start has to be greater than 0 
		start = index_pos - 2
		if start < 0:
			start = 0
		# stop has to be 
		stop = index_pos + 2
		if stop > len(sorted_alphabet):
			stop = -1

		matches = sorted_alphabet[start:stop]


		print "This is segment ratio up top", segment_ratio

		
		proportion_matches.setdefault(img.filename, matches)


	for key, value in proportion_matches.items():
		print key, value 

	return proportion_matches 


# def index(a, x):
#     'Locate the leftmost value exactly equal to x'
#     i = bisect_left(a, x)
#     if i != len(a) and a[i] == x:
#         return i
#     else:
#     	pass

# def find_le(a, x):
#     'Find rightmost value less than or equal to x'
#     i = bisect_right(a, x)
#     if i:
#         return a[i-1]
#     else:
#     	pass

# def find_ge(a, x):
#     'Find leftmost item greater than or equal to x'
#     i = bisect_left(a, x)
#     if i != len(a):
#         return a[i]
#     # raise ValueError
#     pass



def resize_images(bigger_img, smaller_img, new_width, new_height):

	print "This is the new width", new_width
	print "This is the big_img filename", bigger_img.filename
	print "This is the big_img.width before resize", bigger_img.width

	name = bigger_img.filename

	print "This is the name:", name 

	resized_img = bigger_img.resize(new_width, new_height)

	 # this overwrites the template library - should save to temp instead

	print "This is the resized_img.filename", resized_img.filename

	print "This is the new_big.width after resize", resized_img.width

	return resized_img # resized down to new width




# only works when images are identically sized 
def difference_of_images(user_img, template_img): # using XOR in python
	print "This is the difference function: ", user_img.filename, user_img.width, user_img.height
	print "This is the template image in the difference function", template_img.filename, template_img.width, template_img.height
	
	user_matrix = user_img.getNumpy().flatten()
	template_matrix = template_img.getNumpy().flatten()

	difference = [i ^ j for i, j in zip(user_matrix, template_matrix)]
	difference2 = [i ^ j for i, j in zip(template_matrix, user_matrix)]


	difference = difference.count(255)
	difference2 = difference2.count(255)

	
	percent_of_diff = difference/float(len(user_matrix))
	print "This is the percent_of_diff", percent_of_diff
	return percent_of_diff
	#however many times 255 appears in the list
	
	# total_diff = float(len(difference)) + float(len(difference2))
	# pixel_count = float(len(img1)) + float(len(img2))
	# percent_of_diff = total_diff/pixel_count
	# print percent_of_diff
	#1 means complete difference; 0 means complete same

			

		# letters = model.session.query(model.Training_Letter).filter_by(aspect_ratio=aspect_ratio).all()

		# # this gives me a Training Letter object but how do I get the letter ID from this?

		# for item in letters:
		# 	value = item.value
		# 	alphabet = chr(value)
		# 	print alphabet 


		





def main():
	sorted_alphabet = sort_alphabet()
	# directory = 'user_image'
	# add_user_image(directory) # commits user images to database
	p = match_proportions('user_image', sorted_alphabet)
	

	# identify_letter()
	# get_user_images()

if __name__ == "__main__":
	main()





