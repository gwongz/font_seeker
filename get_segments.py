from sys import argv
import PIL

"""Segments image into individual characters"""

def load_image(imgname):
	img = PIL.Image.open(imgname)
	if img.mode != '1':
		img = img.convert('1')

	width = img.size[0]
	height = img.size[1]

	pixels = img.load()
	columns = []
	for y in range(height):
		columns.append([pixels[y,x] for x in range(width)])

	return width, height, columns, img

# def get_image_grid(imgname):
# 	pixels = img.load()
# 	grid = []
# 	for y in range(height):
# 		grid.append([pixels[x,y] for x in range(width)])

# 	return grid 
	# grid[0][0] returns color at (x,y)	
	# don't need this function right now 
	# grid[x][y] = columns[y][x]

def get_column(grid): # stores rows from image grid as columns
	pixels = img.load()
	columns = []
	for y in range(height):
		columns.append([pixels[y,x] for x in range(width)])
	return columns
	# column returns color at coordinate (y,x) - read as 
	# row[4] column[0]


def first_black(width, height, columns, current_col):
	
	while current_col < width:
		if columns[current_col].count(0) >= 1:
			return current_col	
		else:
			current_col +=1
		
	
def all_white(width, height, columns, current_col):
	
	while current_col < width:	
		if columns[current_col].count(255) == width:
			return current_col
		else:
			current_col +=1

	return current_col


def scan_image(width, height, columns):
	"""Finds vertical project of image"""
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

def get_letters(slices, height, img):
	# slices = [(0,0), (1,0)]
	# slices = [(35,0), (67,0)]
	
	segments = [] 
	n=0

	for item in slices:
		if n <= len(slices)-1: 
			
			width = slices[n+1] - slices[n] # width of each crop
			left = slices[n]
			top = 0 
			box = (left, top, left+width, top+height)
			

			output = 'user_crop%s.png' % (n)
			segments.append(output)

			letter = img.crop(box)
			letter.save(output) # saves image to current directory as 'letter'			
		
			n += 2 # increment by 2 because each pair is a set of bounds

		else:
			break

	return segments # returns list of all the cropped and segmented imgs

# should add function to get x bounds

def main():
	script, input_file = argv
	imgname = input_file

	img_width_height_columns = load_image(imgname) # loads basic img information

	width = img_width_height_columns[0]
	height = img_width_height_columns[1]
	columns = img_width_height_columns[2]
	img = img_width_height_columns[3]

	y_bounds = scan_image(width, height, columns)
	segments = get_letters(y_bounds, height, img)
	# segments is a list of all the cropped segments


if __name__== "__main__":
	main()

