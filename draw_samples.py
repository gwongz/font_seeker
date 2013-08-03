import string, re
import os
from PIL import Image, ImageDraw, ImageFont


"""Draws A-Z and a-z for fonts located in "font_files" directory"""

def get_fonts():
	
		fontpath = 'font_files'
		ttfs = os.listdir(fontpath)

		if '.DS_Store' in ttfs:
			ttfs.remove('.DS_Store')

		for font in ttfs:
			fontname = re.sub('\s', '-', font) #filename
			os.rename(path+font, path+fontname)
			shortname = re.search('.+(?=\.)', fontname).group() #name without file ext

			#make font object
			font = Font(name=shortname)
			db_session.add(font)
			db_session.flush()
			db_session.refresh(font)

			load_fixed_font_imgs(font, path)


def draw_alphabet(fontpaths, dirname, fonts):

	for count in range(0,52):
		if count < 26:
			letter = chr(ord('A') + count)
			letter_object = Letter(value=letter, upper=True, pointsize=pointsize, fixed_width=width, fixed_height=height)
			db_session.add(letter_object)
			db_session.commit()

			os.mkdir(root_directory+'/fixed/'+letter+'-upper/')
			os.mkdir(root_directory+'/constrained/'+letter+'-upper/')
		
			
	for letter in string.ascii_uppercase:
		img = Image.new('1', (200,250), 'white')
		fontpath = os.path.join(dirname, font)
		font = ImageFont.truetype(fontpath, 150)
		draw = ImageDraw.Draw(img)
		draw.text((0,0), letter, font=font, fill='black')
		letterpath = os.path.join(dirname, letter)
		print letterpath
		# img.save(letterpath


	
	# fontPath = "font_files"

	# pattern = re.search(".[\w]+", name)
	# name = pattern.group()
	# font = ImageFont.truetype(fontPath, 150)
	# for letter in string.ascii_uppercase:
	# 	img = Image.new('1', (200, 250), 'white')
	# 	draw = ImageDraw.Draw(img)
	# 	draw.text((0,0), letter, font = font, fill= "black")
	# 	fontpath = os.path.join(fonts_directory, )
	

		# img.save('/font_files/%s.%s.png' % (letter, name))
		# will need to decide where in dir to save these images 


def main():
# 	# script, input_file = argv
# 	# fontname = input_file
	dirname = "font_files"
	fonts = []
	
			fonts.append(font)
	

	print fonts
	print fontPath




# if __name__== "__main__":
# 	main()
draw_alphabet('font_files')