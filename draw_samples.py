import string, re
from PIL import Image, ImageDraw, ImageFont

root = "/Users/gwongz/src/hackbright/project/font_files"
fontPath = "/Users/gwongz/src/hackbright/project/font_files/A_CAPPELLA.ttf"

def draw_uppercase(fontPath):
	"""Draws A-Z for font specified in fontPath"""
	name = fontPath.split("/")[-1]
	pattern = re.search(".[\w]+", name)
	name = pattern.group()
	font = ImageFont.truetype(fontPath, 150)
	for letter in string.ascii_uppercase:
		im = Image.new('1', (200, 250), 'white')
		draw = ImageDraw.Draw(im)
		draw.text((0,0), letter, font = font, fill= "black")
		im.save('/Users/gwongz/src/hackbright/project/font_files/%s.%s.png' % (letter, name))
		# will need to decide where in dir to save these images 


draw_uppercase(fontPath)