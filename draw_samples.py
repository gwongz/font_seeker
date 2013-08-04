import os
import string
import PIL
from PIL import Image, ImageDraw, ImageFont



"""Draws uppercase and lowercase samples for fonts located in 'fonts' directory"""

def make_font_directories(root_directory):

	if not os.path.exists(root_directory):
		os.mkdir(root_directory)
	
	ttfs = os.listdir(root_directory) 

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

		
		# draws samples for each font 
		draw_lower(fontpath, shortname, font_directory)
		draw_upper(fontpath, shortname, font_directory+'/upper')



def draw_lower(fontpath, shortname, font_directory): 

	for letter in string.ascii_lowercase:
		letterpath = os.path.abspath(os.path.join(font_directory, letter+'.png'))
		
		# if sample file doesn't already exist, then make one
		if not os.path.exists(letterpath): 
			W, H = (600, 600)
			img = Image.new('1', (W,H), 'white')	
			font = ImageFont.truetype(fontpath, 350) 
			draw = ImageDraw.Draw(img)
			# w, h = draw.textsize(letter)
			# draw.text(((W-w)/4,(H-h)/10), letter, font=font, fill='black')
			draw.text((W/5,H/5), letter, font=font, fill='black')			
			# saves new img to font_directory as 'a.png', 'b.png', etc.	
			img.save(letterpath, quality = 100)

def draw_upper(fontpath, shortname, font_directory):
	
	for letter in string.ascii_uppercase:
		letterpath = os.path.abspath(os.path.join(font_directory, letter+'.png'))
	
		if not os.path.exists(letterpath):
			W, H = (600,600)
			img = Image.new('1', (W,H), 'white')	
			font = ImageFont.truetype(fontpath, 350) 
			draw = ImageDraw.Draw(img)
			# w, h = draw.textsize(letter)
			draw.text((W/5, H/5), letter, font=font, fill='black')			
			# saves new img to font_directory as 'A.png', 'B.png', etc.	
			img.save(letterpath, quality = 100)


def main():

	root_directory = 'templates'
	make_font_directories(root_directory)

if __name__== "__main__":
	main()
