import PIL
from SimpleCV import Image, Color


def make_table(img, width, height):
	"""Creates image grid with y columns and x rows"""

	table = [[ 0 for y in range(width)] for x in range(height) ]
	# populates table with pixel values of img
	for y in range(width):
		for x in range(height):
			table[x][y] = pixels[x, y]

	return table
	# this does same thing as 


def first_column_with_pixel_color(color, start, width, height):
	img = PIL.Image.open('bw.png')
	pixels = img.load()

	for x in range(start, width): # x is the column 
		for y in range(height):

			cpixel = pixels[x,y]
			if cpixel == color:
				# x is column number 
				return x 

	return None

# test prints 		
# first = first_column_with_pixel_color(0, 0)
# second = first_column_with_pixel_color(255, first)
# third = first_column_with_pixel_color(0, second)
# print first, second, third


def scan_image(width, height):
	"""Finds columns where image should be segmented"""
	looking_for = 0 # first look for black
	starting_col = 0 # start with first column
	boundaries = []

	while starting_col != None:

		next_col = first_column_with_pixel_color(looking_for, starting_col, width, height)
		if next_col != None:
			boundaries.append(next_col)
		if next_col == 0: # if you found black in first iteration, start looking for white
			looking_for = 255
		else:
			looking_for = 0	
		starting_col = next_col 


	return boundaries



def main():
	imgname = 'bw.png'
	img = PIL.Image.open(imgname)
	if img.mode != '1':
		img = img.convert('1')
	width = img.size[0]
	height = img.size[1]
	pixels = img.load()
	all_pixels = []
	for x in range(width):	
		for y in range(height):
			cpixel = pixels[x,y]
			all_pixels.append(cpixel)

	

	bounds = scan_image(width, height)
	print bounds 

if __name__== "__main__":
	main()






