import PIL
from SimpleCV import Image, Color


def first_column_with_pixel_color(color, start, width, height, table):
	for y in range(start, width):
		for x in range(height):

			pixel = table[y, x]
			if pixel == color:
				# x is column number 
				return x 

	return None


def scan_image(width, height, table):
	"""Finds columns where image should be segmented"""
	

	looking_for = 0 # first look for black
	starting_col = 0 # start with first column
	boundaries = []

	print "This is initialized looking_for", looking_for
	print "This is initialized starting_col", starting_col


	while starting_col != None:	
		print "This is starting_col at top", starting_col
		print "This is looking_for at top", looking_for
		
		next_col = first_column_with_pixel_color(looking_for, starting_col, width, height, table)
		print "This is next_col", next_col
		
		if next_col != None:
			boundaries.append(next_col)			
			looking_for = 255

		else:
			looking_for = 0
		starting_col = next_col
		
		
		print "This is starting_col at bottom ", starting_col
		print "This is next_col at bottom ", next_col
		print "This is looking_for at bottom ", looking_for	
		

	slices = [(x, 0) for x in boundaries if x!= None] # a list of tuples 
	
	return slices 


def main():
	imgname = 'rockwell_a.png'
	img = PIL.Image.open(imgname)
	if img.mode != '1':
		img = img.convert('1')
	table = img.load()
	width = img.size[0]
	height = img.size[1]
	# print width
	# print height


	slices = scan_image(width, height, table)

  

if __name__ == "__main__":
	main()

 


 # def get_letter(img, slices):
# 	"""Crops image at slices coordinates and saves"""
# 	# opens cropped image 
# 	img = PIL.Image.open(img)
# 	height = img.height
# 	width = img.width

# 	for item in slices:
# 		n = slices.index(item)
# 		width = slices[n+1][0] - slices[n][0]

# 		if n+1 < len(slices)-1:
# 			print "This is the item: ", item
# 			print "This is the width: ", width
# 			print "This is n", n 
# 			letter = cropped_image.crop(item[0], item[1] width, height)
# 			letter.save('letter.%s') % (n)

# 		else:
# 			break
	
	# this is an image cropped from original 
	# do i need to return anything here if I'm just saving an image?

# letter = get_letter('rockwell_a.png', slices)

# def process_letter(img): # takes segmented letter as input
# 	"""Crops segmented letter so it is optimized for matching"""
# 	img = Image(img)
# 	binarize = img.binarize() # SimpleCV img class
# 	blobs = img.findBlobs() # uses SimpleCV blobs fcn
# 	bounds = blobs[-1].boundingBox() # SimpleCV fcn
# 	img = img.crop(bounds)
# 	img.save('user_img.png') # returns a cropped image object 



