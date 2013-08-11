import os
import string
import shutil

from PIL import Image, ImageOps, ImageFont, ImageDraw, ImageChops
import SimpleCV as cv 
# from SimpleCV import Image





def make_directories(srcdir, destdir): 

	root = "."
	ttfs = os.listdir(srcdir)

	if '.DS_Store' in ttfs:
		ttfs.remove('.DS_Store')

	# os.chdir(directory)

	for f in ttfs:
		fontpath = os.path.join(srcdir, f)
		full_name = f.split('.')[0:-1]
		full_name = f.split('-')[0:-1]
		font_name = "".join(full_name)
		# font_directory = os.path.join(directory, font_name)

		# if os.path.exists(font_directory):
		# 	shutil.rmtree(font_directory)

		currentpath = os.getcwd()
		newpath = os.path.join(currentpath, destdir)
		
		font_directory = os.path.join(newpath, font_name)

		if os.path.exists(font_directory):
			shutil.rmtree(font_directory)

		os.mkdir(font_directory)
	
		upper = os.path.join(font_directory, 'upper')
		lower = os.path.join(font_directory, 'lower')
	
		os.mkdir(upper)
		os.mkdir(lower)


		print "Font directory: ", font_directory
		print "Fontpath: ", fontpath 

	
		draw_lower(fontpath, font_directory)
	# makes uppercase and lowercase directories for font samples 

def draw_lower(fontpath, font_directory):



	# fontpath = 'fonts/Arial.ttf'
	W, H = 100, 100
	font = ImageFont.truetype(fontpath, 75)
	# font_directory = os.path.join('fonts/Arial', 'lower')

	lower_directory = os.path.join(font_directory, 'lower')
	print "This is the lower_directory:", lower_directory

	# os.chdir(lower_directory)
	
	for letter in string.ascii_lowercase:
		letterfile = letter+'.png'
		letterpath = os.path.join(lower_directory, letterfile)
		
		img = Image.new('1', (W,H), 'white')	
		draw = ImageDraw.Draw(img)
		w, h = draw.textsize(letter, font=font)
	
		print "This is the w, h:", w, h # centers the text 
			# w, h = draw.textsize(letter)
			# draw.text(((W-w)/4,(H-h)/10), letter, font=font, fill='black')

		# draw.text((W/2)-w, (H/2)-h, letter, font=font, fill='black')	
		draw.text(((W-w)/2, (H-h)/2), letter, font=font, fill='black')			
			# saves new img to font_directory as 'a.png', 'b.png', etc.	

		new_img = img.save(letterpath)



# Load the image
def constrained (mypath):

	
	files = os.listdir(mypath)
	if '.DS_Store' in files:
		files.remove('.DS_Store')

	for f in files:
		location = os.path.abspath(os.path.join(mypath, f))
		file_url = os.path.join(mypath, f)
		name = str(file_url)

		img = cv.Image(location).invert()
		adaptimg = img.adaptiveScale((20, 20), cv.Color.WHITE)
		adaptimg.save(name)


def crop_at_bounds(mypath):
	
	segments = os.listdir(mypath)

	if '.DS_Store' in segments:
		segments.remove('.DS_Store')

	for imgfile in segments:
		location = os.path.abspath(os.path.join(mypath, imgfile))
		file_url = os.path.join(mypath, imgfile)
		name = str(file_url)
		print location 
		img = cv.Image(location)
		
		
		blobs = img.binarize().findBlobs()
	
		if blobs != None:
			bounds = blobs[-1].boundingBox()
			crop = img.crop(bounds).save(name)

		if blobs == None:
			os.remove(file_url)



def main():

	make_directories('testing_font_directories', 'font_letters')
	# root = 'ocr_alphabet/Arial'
	# make_directories(root)
	# ocr_samples = draw_lower()
	# crop_at_bounds('ocr_alphabet/Arial/lower')
	# constrained('ocr_alphabet/Arial/lower')

	# root = 'user_image'
	# crop_at_bounds('user_image')
	# constrained('user_image')

	
	# letter_samples = draw_lower()
	# crop_at_bounds('fonts/Arial/lower')
	# constrained('fonts/Arial/lower')


if __name__ == "__main__":
	main()




