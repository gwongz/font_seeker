import os
import string
import shutil
from PIL import Image, ImageOps, ImageFont, ImageDraw, ImageChops


"""Draws upper and lower letter samples with ttf files in 'font_files' and 'ocr_alphabet' directories"""

def make_letter_samples(srcdir, destdir): 

	ttfs = os.listdir(srcdir)

	if '.DS_Store' in ttfs:
		ttfs.remove('.DS_Store')

	for f in ttfs:
		fontpath = os.path.join(srcdir, f)
		full_name = f.split('.')[0:-1]
		if '-' in full_name:
			full_name = f.split('-')[0:-1]
		font_name = "".join(full_name)

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
		draw_upper(fontpath, font_directory)

def draw_lower(fontpath, font_directory):

	W, H = 100, 100
	font = ImageFont.truetype(fontpath, 75)

	lower_directory = os.path.join(font_directory, 'lower')
	print "This is the lower_directory:", lower_directory
	
	for letter in string.ascii_lowercase:
		letterfile = letter+'.png'
		letterpath = os.path.join(lower_directory, letterfile)
		
		img = Image.new('1', (W,H), 'white')	
		draw = ImageDraw.Draw(img)
		w, h = draw.textsize(letter, font=font) # centers the text 
	
		print "This is the w, h:", w, h  
		draw.text(((W-w)/2, (H-h)/2), letter, font=font, fill='black')			

		new_img = img.save(letterpath)

def draw_upper(fontpath, font_directory):

	W, H = 100, 100
	font = ImageFont.truetype(fontpath, 75)

	upper_directory = os.path.join(font_directory, 'upper')
	
	for letter in string.ascii_uppercase:
		letterfile = letter+'.png'
		letterpath = os.path.join(upper_directory, letterfile)
		
		img = Image.new('1', (W,H), 'white')	
		draw = ImageDraw.Draw(img)
		w, h = draw.textsize(letter, font=font)
	
		print "This is the w, h:", w, h # centers the text 
		draw.text(((W-w)/2, (H-h)/2), letter, font=font, fill='black')			

		new_img = img.save(letterpath)


def main():

	make_letter_samples(srcdir='ocr_font_files', destdir='ocr_alphabet')
	# make_letter_samples(srdir='font_files', destdir='font_letters')



if __name__ == "__main__":
	main()




