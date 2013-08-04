"""Loads fonts from local directory into database"""
 
import os 
import re 
from SimpleCV import Image


def get_samples(directory):

	samples_dict = {}

	# looks for .png sample files in fonts directory and appends to dict by letter 
	for dirpath, dirnames, fnames in os.walk(directory):
	    for f in fnames:
	        if f.endswith('.png'):
	        	location = os.path.join(dirpath, f)
	        	letter = f.split('.')[0]
	        	samples_dict.setdefault(location, letter)
	  				
	return samples_dict

def crop_letters(samples_dict):
	for key in samples_dict.iterkeys():
		img = Image(key)
		binarize = img.binarize()
		blobs = binarize.findBlobs()
		bounds = blobs[-1].boundingBox()
		crop = img.crop(bounds)
		crop.save(key)

def load_letters(samples_dict):

	for key in samples_dict.iterkeys():
		file_url = key
		value = samples_dict[key]
		print key, value 








	    
def main():
	directory = 'templates'
	font_samples = get_samples(directory)
	
	crop_letters(font_samples)


if __name__ == "__main__":
	main()
	        	 









# img = Image('fonts/Arial/a.png')
# print img.height 

# def main(session):
# 	directory = 'fonts'
# 	crop_samples(directory)

	

# if __name__ == "__main__":
# 	s = model.session
# 	main(s)
