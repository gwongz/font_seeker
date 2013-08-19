import os
import SimpleCV as cv 
from PIL import Image, ImageOps

"""Image processing functions run on ocr_alphabet and font_letters before seeding database"""



def crop_at_bounds(srcdir):

	for dirpath, dirnames, fnames in os.walk(srcdir):
		for basename in fnames:
			if basename.endswith('.png'):
				
				location = os.path.abspath(os.path.join(dirpath, basename))
				file_url = os.path.join(dirpath, basename)
				name = str(file_url)

				img = cv.Image(location)
				blobs = img.binarize().findBlobs()
	
				if blobs != None:
					bounds = blobs[-1].boundingBox()
					crop = img.crop(bounds).save(name)

				if blobs == None:
					os.remove(file_url)

def make_constrained(srcdir):

	for dirpath, dirnames, fnames in os.walk(srcdir):
		for basename in fnames:
			if basename.endswith('.png'):

				location = os.path.abspath(os.path.join(dirpath, basename))
				file_url = os.path.join(dirpath, basename)
				name = str(file_url)
				try:
					img = cv.Image(location).binarize()
					adaptimg = img.adaptiveScale((40, 40), cv.Color.WHITE)

					# adaptimg = img.adaptiveScale((20, 20), cv.Color.WHITE)
					adaptimg.save(name)

				except:
					print "It looks like there was an error for this file: ", file_url
					



def main():

	crop_at_bounds(srcdir='ocr_alphabet')
	crop_at_bounds(srcdir='font_letters')
	make_constrained(srcdir='ocr_alphabet')
	make_constrained(srcdir='font_letters')




if __name__ == "__main__":
	main()