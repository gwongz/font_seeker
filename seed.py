"""Loads fonts from local directory into database"""
 
import os 
import re 
from SimpleCV import Image
import model 


def get_templates(directory):

	templates_dict = {}

	# looks for .png sample files in fonts directory and appends to dict by letter 
	for dirpath, dirnames, fnames in os.walk(directory):
	    for f in fnames:
	        if f.endswith('.png'):
	        	location = os.path.join(dirpath, f)
	        	letter = f.split('.')[0]
	        	templates_dict.setdefault(location, letter)
	  				
	return templates_dict

def crop_letters(templates_dict):
	for key in templates_dict.iterkeys():
		img = Image(key)
		if img.height > 400:
			binarize = img.binarize()
			blobs = binarize.findBlobs()
			bounds = blobs[-1].boundingBox()
			crop = img.crop(bounds)
			crop.save(key)
			width = crop.width
			height = crop.height

		else:
			width = img.width
			height = img.height

		current_value = templates_dict[key]
		new_array = [current_value, width, height]	
		# resets value of keys in dict so they return letter, width, height 
		templates_dict[key] = new_array

		
	return templates_dict

def load_letters(session, letters_dict):

	for key in letters_dict.iterkeys():
		file_url = key
		font_name = key.split('/')[1]
		letter_of_alphabet = letters_dict[key][0]
		value = ord(letter_of_alphabet)
		width = letters_dict[key][1]
		height = letters_dict[key][2]


		letter = model.Letter(value = value,
								file_url = file_url,
								font_name = font_name,
								height = height,
								width = width)

		session.add(letter)
	session.commit()

		# if 65 <= value <= 90:
		# 	upper = True 










	    
def main(session):
	directory = 'templates'
	templates_dict = get_templates(directory)
	letters_dict = crop_letters(templates_dict)
	load_letters(session, letters_dict)

if __name__ == "__main__":
	
	main(model.session)
	        	 









	

# if __name__ == "__main__":
# 	s = model.session
# 	main(s)
