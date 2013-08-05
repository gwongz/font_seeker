
import os
from sys import argv
from bisect import bisect_right
# from PIL import Image, ImageChops
from SimpleCV import Image
import seed
import model 


"""Identifies letter of alphabet for each segment stored in 'user' directory"""


def clear_user_image(session):
	user_img = model.session.query(model.User_Image).all()
	
	for imgfile in user_img:
		session.delete(imgfile)
		session.commit()


def add_user_image(directory):

	# clear db before storing what's been added to user directory	
	session = model.session
	clear_user_image(session)

	segments = os.listdir(directory)
	if '.DS_Store' in segments:
			segments.remove('.DS_Store')


	for imgfile in segments:
		# adds each segment to database as User_Image object 
		img_location = os.path.abspath(os.path.join(directory, imgfile))
		file_url = os.path.join(directory, imgfile)
		name = str(file_url)

		img = Image(img_location)
		blobs = img.binarize().findBlobs()
		bounds = blobs[-1].boundingBox()
		crop = img.crop(bounds).save(name)

		seed.load_user_image(session, img_location, file_url) # location is abs path, file_url is relative path 


def identify_letter():

	user_imgs = model.session.query(model.User_Image).all()
	user_aspect_ratios = []
	
	for img in user_imgs:
		user_aspect_ratios.append(img.aspect_ratio) # do i want to store these as a list or dictionary? 

	alphabet = model.session.query(model.Training_Letter).all()
	alphabet_aspect_ratios = []
	for letter in alphabet:
		alphabet_aspect_ratios.append(letter.aspect_ratio)



	

	sorted_alphabet = sorted(alphabet_aspect_ratios)

	# i should map sorted alphabet to a dictionary 

	# threshold = 0.5
	for ratio in user_aspect_ratios:
		
		threshold = 0.05
		ratio_upper = ratio+threshold
		ratio_lower = ratio-threshold

		matches = [x for x in sorted_alphabet if x > ratio_lower and x < ratio_upper]

		for match in matches:
			

		# letters = model.session.query(model.Training_Letter).filter_by(aspect_ratio=aspect_ratio).all()

		# # this gives me a Training Letter object but how do I get the letter ID from this?

		# for item in letters:
		# 	value = item.value
		# 	alphabet = chr(value)
		# 	print alphabet 


		break











def find_le(a, x):
    'Find rightmost value less than or equal to x'
    i = bisect_right(a, x)
    if i:
        return a[i-1]
    raise ValueError





# def load_training_alphabet(letter_value):

# 	letter = model.session.query(model.Trainer).filter(model.Trainer.value==letter_value).first()
# 	location = letter.file_url
# 	value = letter.value 

	
# 	return location # opens up 'A' in the training alphabet
	

	




# def identify_letter(segments):
# 	"""Identifies what letter a segment is"""
# 	# < len(segments):
# 	# n=0
# 	# while n ==0: 
# 	match = False

# 	while match not True:
# 		img1 = Image(segments[0])
# 		letter_value = 65
# 		img2_location = load_training_alphabet(letter_value)
# 		img2 = Image(image2_location)
		
# 		width = max(img1.width, img2.width)
# 		height = max(img1.height, img2.height)

# 		# if img1 is bigger, resize it down to img2 size
# 		if img1.size() > img2.size():
# 			img = img1.resize(width, height)

# 		else:
# 			img = img2.resize(width, height)







		# if img1[1]
		# # see which one is bigger or smaller and resize 

		# difference_of_images(img1, img2)




		# don't forget to increment letter value
		# n+=1 # increments n 

# only works when images are identically sized 
def difference_of_images(img1, img2): # using XOR in python

	
	difference = [i ^ j for i, j in zip(img1, img2)]
	difference2 = [i ^ j for i, j in zip(img2, img1)]


	difference = difference.count(255)
	difference2 = difference2.count(255)

	
	percent_of_diff = difference/float(len(img1))
	return percent_of_diff
	#however many times 255 appears in the list
	
	# total_diff = float(len(difference)) + float(len(difference2))
	# pixel_count = float(len(img1)) + float(len(img2))
	# percent_of_diff = total_diff/pixel_count
	# print percent_of_diff
	#1 means complete difference; 0 means complete same

	










def main():
	# directory = 'user'
	# add_user_image(directory)
	identify_letter()

if __name__ == "__main__":
	main()





