import os
import string
import PIL
from SimpleCV import Image, ImageSet
# from SimpleCV import Image

# from PIL import Image, ImageDraw, ImageFont




"""Draws uppercase and lowercase samples for fonts located in 'fonts' directory"""

def make_templates(root_directory):

	if not os.path.exists(root_directory):
		os.mkdir(root_directory)
	
	ttfs = os.listdir(root_directory) 

	if ttfs == []:
		print "There are no font files in this directory."
		return

	if '.DS_Store' in ttfs:
			ttfs.remove('.DS_Store')

	for fontfile in ttfs:
		# fontpath is where the ttf file is located 
		fontpath = os.path.join(root_directory, fontfile) 
	
		# shortname is just name of the font 
		(shortname, extension) = os.path.splitext(fontfile)
		font_directory = os.path.join(root_directory, shortname)

		# makes new directory for font if it doesn't already exist
		if not os.path.exists(font_directory): # if the font_directory doesn't exist, make it
			os.mkdir(font_directory) # makes directory for each font 
			# makes sub-directory for uppercase samples
			os.mkdir(font_directory+'/upper') # makes a sub folder for uppercase fonts

		lower = string.ascii_lowercase
		upper = string.ascii_uppercase
		
		# draws samples for each font 
		draw_letters(fontpath, shortname, font_directory, lower)
		draw_letters(fontpath, shortname, font_directory+'/upper', upper)



def draw_letters(fontpath, shortname, font_directory, letter_range): 

	for letter in letter_range:
		letterpath = os.path.abspath(os.path.join(font_directory, letter+'.png'))
		
		# if sample file doesn't already exist, then make one
		if not os.path.exists(letterpath): 
			W, H = (600, 600)
			img = PIL.Image.new('1', (W,H), 'white')	
			font = PIL.ImageFont.truetype(fontpath, 350) 
			draw = PIL.ImageDraw.Draw(img)
			# w, h = draw.textsize(letter)
			# draw.text(((W-w)/4,(H-h)/10), letter, font=font, fill='black')
			draw.text((W/5,H/5), letter, font=font, fill='black')			
			# saves new img to font_directory as 'a.png', 'b.png', etc.	
			img.save(letterpath, quality = 100)

def crop_letters(directory):

	# looks for .png sample files in fonts directory and appends to dict by letter 
	for dirpath, dirnames, fnames in os.walk(directory):
	    for f in fnames:
	        if f.endswith('.png'):
	        	location = os.path.join(dirpath, f)
	        	img = Image(location) # uses SimpleCV Image class 
	        	blobs = img.binarize().findBlobs()
	        	bounds = blobs[-1].boundingBox()
	        	img.crop(bounds).save(location)
	        
def main():

	# root_directory = 'templates'
	# make_templates(root_directory)
	training_alphabet = make_templates('training_alphabet')
	crop_letters('training_alphabet')


if __name__== "__main__":
	main()
