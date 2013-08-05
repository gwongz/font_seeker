"""Loads fonts from local directory ('templates' and 'training_alphabet') into database"""
 
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

def get_image_info(templates_dict):
	# updates dictionary with more info for loading to db

	for key in templates_dict.iterkeys():
		img = Image(key)
		width = img.width
		height = img.height
		current_value = templates_dict[key]
		new_array = [current_value, width, height]	
		# resets value of keys in dict so they return letter, width, height 
		templates_dict[key] = new_array

	return templates_dict


def load_letters(session, image_info): #image_info is a dictionary

	for key in image_info.iterkeys():
		file_url = key
		font_name = key.split('/')[1]
		letter_of_alphabet = image_info[key][0]
		value = ord(letter_of_alphabet)
		width = image_info[key][1]
		height = image_info[key][2]
		aspect_ratio = round(float(width)/float(height), 4)

		letter = model.Letter(value = value,
								file_url = file_url,
								font_name = font_name,
								width = width,
								height = height,
								aspect_ratio = aspect_ratio)

		session.add(letter)
	session.commit()

		# if 65 <= value <= 90:
		# 	upper = True 


def load_training_letters(session, image_info):

	for key in image_info.iterkeys():
		file_url = key
		letter_of_alphabet = image_info[key][0]
		value = ord(letter_of_alphabet)
		width = image_info[key][1]
		height = image_info[key][2]
		aspect_ratio = round(float(width)/float(height), 4)

		training_letter = model.Training_Letter(value = value,
								file_url = file_url,
								width = width,
								height = height,
								aspect_ratio = aspect_ratio)

		session.add(training_letter)
	session.commit()

def load_user_image(session, img_location, file_url):
	img = Image(img_location)
	width = img.width
	height = img.height
	aspect_ratio = round(float(width)/float(height), 4)

	user_image = model.User_Image(file_url = file_url,
								width = width,
								height = height,
								aspect_ratio = aspect_ratio)

	session.add(user_image)
	session.commit()


def main(session):
	# directory = 'training_alphabet' or directory = 'templates'
	alphabet_dict = get_templates(directory)
	alphabet_info = get_image_info(alphabet_dict)	
	load_training_letters(session, alphabet_info)


if __name__ == "__main__":
	
	main(model.session)
	        	 


