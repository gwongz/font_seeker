import PIL
from SimpleCV import Image

"""Takes image and finds boundaries where it needs to be cropped"""

def load_image(imgname):
	img = PIL.Image.open(imgname)
	if img.mode != '1':
		img.convert('1')

	width = img.size[0]
	height = img.size[1]

	pixels = img.load()
	columns = []
	for y in range(height):
		columns.append([pixels[y,x] for x in range(width)])

	return width, height, columns

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
		if columns[current_col].count(0) > 1:
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
	boundaries = []
	current_col=0
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
	
	return boundaries


def main():
	imgname = 'test.png'
	img_width_height_columns = load_image(imgname) # loads basic img information

	width = img_width_height_columns[0]
	height = img_width_height_columns[1]
	columns = img_width_height_columns[2]



	
	bounds = scan_image(width, height, columns)
	print bounds 


	



if __name__== "__main__":
	main()

