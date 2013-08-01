import PIL
from SimpleCV import Image, Color


# def make_table(img, width, height):
# 	"""Creates image grid with y columns and x rows"""

# 	table = [[ 0 for y in range(width)] for x in range(height) ]
# 	# populates table with pixel values of img
# 	for y in range(width):
# 		for x in range(height):
# 			table[x][y] = pixels[x, y]

# 	return table
	


def first_column_with_pixel_color(color, start, width, height, imgname):
	img = PIL.Image.open(imgname)
	pixels = img.load()

	for x in range(start, width): # x is the column 
		for y in range(height):

			cpixel = pixels[x,y]
			if cpixel == color:
				# x is column number 
				return x 

	return None


def scan_image(width, height, imgname):
	"""Finds columns where image should be segmented"""
	looking_for = 0 # first look for black
	current_col = 0 # start with first column
	boundaries = []

	flag = 0

	

	while current_col != None:



		next_col = first_column_with_pixel_color (looking_for, current_col, width, height, imgname)
		print "Color found in column - ", next_col
		if next_col == None:
			break

		if next_col != None:
			boundaries.append(next_col)
		# if next_col == looking_for: # if you found black in first iteration, start looking for white
			
		if next_col == 0:
			looking_for = 255
			current_col = next_col

		elif looking_for == 255: 
			looking_for = 0	
			current_col = next_col + 1
		else:
			looking_for = 255
			current_col = next_col + 1

		print "Current column= ", current_col
		print "Looking for color = ", looking_for

		# if current_col == 14:
		# 	flag += 1

		# if flag == 10:
		# 	break



	return boundaries



def main():
	imgname = 'temp.png'
	img = PIL.Image.open(imgname)
	if img.mode != '1':
		img = img.convert('1')
	# img.save('temp.png')
	width = img.size[0]
	height = img.size[1]
	pixels = img.load()
	all_pixels = []
	for x in range(width):	
		for y in range(height):
			cpixel = pixels[x,y]
			all_pixels.append(cpixel)

	

	bounds = scan_image(width, height, imgname)
	print bounds 

if __name__== "__main__":
	main()






