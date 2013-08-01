""" Figuring out how to use SimpleCV to crop blobs"""

from SimpleCV import Image, Color
 
# cropping blob from letter segment
# img = Image('helvetica_A.png')
# binarize = img.binarize()
# binarize.save('binarize.png')
# blobs = img.findBlobs()
# bounds = blobs[-1].boundingBox()
# crop = img.crop(bounds)
# crop.save('blob.png') # only works for segmented blob

# no way to tell image mode so must binarize before finding blob
# why is only one character seen as blob

img = Image('blarry.png')

blobs = img.findBlobs()
print blobs


print img.height
print img.width
 
# get pixel value at (x,y)
# pixel = img[10, 10]

# centroid()
# SUMMARY
# Return the centroid (mass-determined center) of the blob. 
# Different from bounding box center.
# RETURNS
# (x,y) tuple that is the center of mass of the blob. 

# splitting an image into quadrants
# img = Image('blarry.png')
# print img.height
# print img.width

# quads = img.split(2,2)

# split(cols, rows)
# SUMMARY This method can be used to break image into a series of image chunks. 
# Splits the image into a cols x rows 2d array


        

	
 
# gets coordinates for where to crop
# bounds = blobs[-1].boundingBox()
# bounds2 = blobs[-2].boundingBox()

 
# crops image
# cropped = img.crop(bounds)
# cropped.save('helv_arial.bounds.png')
# parameters are (x, y, width of crop, height of crop)
# parameters obtained from slices from get_segments.py
# croppedright = img.crop(5,0,5,img.height)
# croppedleft = img.crop(0,0,5,img.height)


# saves image
# croppedright.save('cropped_right.png')
# croppedleft.save('cropped_left.png')

# Extra functions to explore:
# width of minimum bounding rectangle of blob
# print "This is the rectangle bounding box", blobs[-1].boundingBox()
# [x, y, w, h] -- x, y is the top left coordinate; w



# won't work because of Pygame module
# blobs[-1].drawRect(color=Color.RED, width = -1, alpha = 128)


# print "This is min Rec width:", blobs[-1].minRectWidth()
# print "This is min Rec height:", blobs[-1].minRectHeight()


# returns corners for smallest rectangle to enclose blob
# print blobs[-1].minRect()


