from sys import argv
import PIL
from SimpleCV import Image

"""Takes image and finds boundaries where it needs to be cropped"""

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
	boundaries = []
	current_col = 0

	while current_col < width and current_col != None:
		
		
		next_col = first_black(width, height, columns, current_col)
		
		print "This is next_col after finding first black", next_col
		
		if next_col == None:
			break # there is no black - prevents infinite loop 

		if next_col != None: # if there is black, add and move on
			boundaries.append(next_col)
			current_col = next_col
		
			white_col = all_white(width, height, columns, current_col) # change looking for to white
			if white_col != None: # if there is an all white column
				boundaries.append(white_col)
				current_col = white_col # reset starting point for scanning

		print "Boundaries at bottom of while loop", boundaries
		print "current_col at bottom of while loop", current_col

	slices = [(x, 0) for x in boundaries if x!= None] # a list of tuples, (x,y) where splits are 
	
	return slices

def get_letter(slices, height, imgname):
	# slices = [(0,0), (1,0)]
	# slices = [(35,0), (67,0)]




	n=0
	
	while n < len(slices)-1:
		print "This is n at the start: ", n
		for item in slices:
			print "This is n at the top of for loop: ", n
			print "This is the item at the top of loop: ", item
			# print "Item[n]: ", item[n]
			# print "Item[n+1]: ", item[n+1]
			width = (slices[n+1][0]) - (slices[n][0]) # width of each crop
			# print "Width: ", width
			print "Width at top of loop for n: ", width, n 

			
			# width = slices[1][0] - slices[0][0]
			# width = 1-0 = 1

			# if 1 <= 1: True 

			# print "This is item[n]: ", item[n]
			box = (item[n], item[n+1], width, height)
			# print box
			print "Box at the top of the loop:", box 
			if n+1 <= len(slices)-1: 
				
			
				img = PIL.Image.open(imgname) # how can I avoid reopening the img?
				if img.mode != '1':
					img.convert('1')
				letter = img.crop(box)
				letter.save('user_crop.png') # saves image to current directory as 'letter'
			
				n += 2

				if n > len(slices)-1:
					break

			else:
				break



def main():
	script, input_file = argv
	imgname = input_file

	img_width_height_columns = load_image(imgname) # loads basic img information

	width = img_width_height_columns[0]
	height = img_width_height_columns[1]
	columns = img_width_height_columns[2]

	slices = scan_image(width, height, columns)
	print "These are the bounds", slices 

	get_letter(slices, height, imgname)



if __name__== "__main__":
	main()

