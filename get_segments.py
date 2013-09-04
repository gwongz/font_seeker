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
	
	os.remove('inverted.png')
	return width, height, columns, newimg

def first_black(width, height, columns, current_col):
	# returns None if no columns with black pixels
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

def scan_image(width, height, columns):
	boundaries = []
	current_col = 0
	while current_col < width and current_col != None:
		next_col = first_black(width, height, columns, current_col)
		if next_col == None:
			print "No black pixels were found"
			break # prevents infinite loop 

		if next_col != None: # if there is black, add and move on
			boundaries.append(next_col)
			current_col = next_col
			white_col = all_white(width, height, columns, current_col) # change looking for to white
			if white_col != None: 
				boundaries.append(white_col)
				current_col = white_col # reset starting point for scanning
	return boundaries

def get_segments(slices, height, img):
	# if os.path.exists('user_image'):
	# 	rmtree('user_image')
	# os.mkdir('user_image')
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
			letter.save('user_image/' + output) 

			n += 2 # increment by 2 because each pair is a set of bounds
		else:
			break
	return segments 

def main(img_url):

	r = urllib.urlretrieve(img_url, 'temp_user_img.png')
	imgname = 'temp_user_img.png'

	img_width_height_columns = load_image(imgname) # loads basic img information
	width = img_width_height_columns[0]
	height = img_width_height_columns[1]
	columns = img_width_height_columns[2]
	img = img_width_height_columns[3]

	y_bounds = scan_image(width, height, columns)

	if y_bounds:
		segments = get_segments(y_bounds, height, img)
	
	else:
		segments = []

	
	os.remove(imgname)
	return segments



if __name__== "__main__":
	main()
