import os, urllib
from shutil import rmtree 
from sys import argv
from PIL import Image
import SimpleCV as cv
import requests 

import model 

"""Segments image into individual characters and saves to user_image directory"""


def load_image(imgname):
	img = cv.Image(imgname)
	binarized = img.binarize()
	inverted = binarized.invert().save('inverted.png')

	newimg = Image.open('inverted.png').convert('1')
	pixels = newimg.load()
	width = newimg.size[0]
	height = newimg.size[1]
	columns = []
	for y in range(width):
		columns.append([pixels[y,x] for x in range(height)])
		# column returns color at coordinate (y,x) - read as 
		# row[4] column[0]
	os.remove('inverted.png')

	# img = Image.open(imgname).convert('1')
	# pixels = img.load()
	# width = img.size[0]
	# height = img.size[1]
	# columns = []
	# for y in range(width):
	# 	columns.append([pixels[y,x] for x in range(height)])
		# column returns color at coordinate (y,x) - read as 
		# row[4] column[0]

	return width, height, columns, newimg


def first_black(width, height, columns, current_col):

	while current_col < width:
		if columns[current_col].count(0) >= 1:
			return current_col	
		else:
			current_col +=1


def all_white(width, height, columns, current_col):

	while current_col < width:	
		if columns[current_col].count(255) == height:
			return current_col
		else:
			current_col +=1

	return current_col

# def first_black_row(width, height, rows, current_row):
# 	while current_row < height:
# 		if rows[current_row].count(0) >= 1:
# 			return current_row
# 		else:
# 			current_row += 1

# def all_white_row(width, height, rows, current_row):
# 	while current_row < height:
# 		if rows[current_row].count(255) == width:
# 			return current_row
# 		else:
# 			current_row +=1
# 	return current_row

def scan_image(width, height, columns):
	"""Finds vertical projection of image"""
	boundaries = []
	current_col = 0

	while current_col < width and current_col != None:

		next_col = first_black(width, height, columns, current_col)
		if next_col == None:
			break # there is no black - prevents infinite loop 

		if next_col != None: # if there is black, add and move on
			boundaries.append(next_col)
			current_col = next_col

			white_col = all_white(width, height, columns, current_col) # change looking for to white
			if white_col != None: # if there is an all white column
				boundaries.append(white_col)
				current_col = white_col # reset starting point for scanning

	# slices = [(x, 0) for x in boundaries if x!= None] # a list of tuples, (x,y) where splits are 
	return boundaries

# def get_x_bounds(width, height, rows):
# 	boundaries = []
# 	current_row = 0

# 	while current_row < height and current_row != None:
# 		next_row = first_black_row(width, height, rows, current_row)
# 		if next_row == None:
# 			break

# 		if next_row != None:
# 			boundaries.append(next_row)
# 			current_row = next_row

# 			white_row = all_white_row(width, height, rows, current_row)
# 			if white_row != None:
# 				boundaries.append(white_row)
# 				current_row = white_row
# 	print "These are the x bounds", boundaries
# 	return boundaries 

def get_segments(slices, height, img):
	# slices = [(0,0), (1,0)]
	# slices = [(35,0), (67,0)]
	if os.path.exists('user_image'):
		rmtree('user_image')

	os.mkdir('user_image')

	# need to add a fcn to clear the contents of 'user_image folder if it exists'

	segments = [] 
	n=0

	for item in slices:
		if n <= len(slices)-1: 

			width = slices[n+1] - slices[n] # width of each crop
			left = slices[n]
			top = 0 
			box = (left, top, left+width, top+height)


			output = 'segment_%s.png' % (n)
			segments.append(output)

			letter = img.crop(box)
			letter.save('user_image/' + output) # saves image to user_image directory as 'segment_0.png'			

			n += 2 # increment by 2 because each pair is a set of bounds

		else:
			break

	return segments # returns list of all the cropped and segmented imgs

def main(img_url):

	r = urllib.urlretrieve(img_url, 'temp_user_img.png')
	imgname = 'temp_user_img.png'

	img_width_height_columns = load_image(imgname) # loads basic img information
	width = img_width_height_columns[0]
	height = img_width_height_columns[1]
	columns = img_width_height_columns[2]
	img = img_width_height_columns[3]

	y_bounds = scan_image(width, height, columns)
	segments = get_segments(y_bounds, height, img)

	if len(segments) <= 1 or None:
		message = "Oh, snap. I can't segment your image. Want to try another image where the text is more spaced out?"


	else:
		message = "Your image has been segmented. Now let's process it."
	
	
	os.remove(imgname)
	return message

	# segments is a list of all the cropped segments


if __name__== "__main__":
	main()
