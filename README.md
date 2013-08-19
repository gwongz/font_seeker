FontSeeker
==========

Have you ever walked by a poster or sign and wanted to know what font the designer used? That happens to me a lot and it’s how this project came to be. FontSeeker was envisoned to be a Shazam for font identification. It takes an image, segments it into glyphs and uses a template-based approach to make a match against a database of font samples (currently just over 100) collected from Font Squirrel and fonts I already owned. FontSeeker was built with Python, Flask, PIL, SimpleCV and SQLAlchemy and uses AJAX on the front end. 

###File Tree
- draw_fonts.py: Uses PIL to draw lowercase and uppercase templates of each font, the OCR alphabet and specimen messages to return to user upon successful match.<br>
- process_images.py: Uses SimpleCV to crop an image to bounds and resize it to a fixed size while maintaining its aspect ratio.<br>
- model.py and seed.py: Creates schema for database and loads fonts, font templates and OCR training letters into database.<br>
- get_segments.py: Converts an image into a binary image and crops the image in locations where all-white columns are identified.<br>
- ranked_match.py: Segmented user images are compared against OCR alphabet and given a letter classification. Each segment is then compared against all the fonts for that letter classification. If the XOR difference meets a certain threshold, it is added to a font table. Fonts are then ranked based on the lowest average XOR difference.

###User Interface
The front end uses HTML5 and CSS. It uses Javascript to make an asynchronous call to the server. <br>
![Alt text](/screenshots/fontseeker.png "User interface")

###Template-based Approach

Imaging libraries such as SimpleCV have powerful tools for extracting features from images, but I hadn’t worked with images before so I decided to start with template matching to understand the basic mechanics of image processing.

Since an image can be converted to a 2D array of black and white pixels, character and font recognition can be made by performing a pixel-by-pixel comparison between input glyphs and template glyphs once segmentation has occurred. 

Currently the process time isn't ideal but I've been working on refactoring the code to reduce the number of wasteful matches during font comparison. For instance, the latest version:

- throws out segments which have a high OCR XOR difference value 
- skips font matches when the letter is likely to cause more errors than its removal would (e.g., segments identified as a "I", "i", or "l")
- process more image data before matching occurs. The number of black pixels in each template image can be calculated and loaded in the database before the match process begins. That way, if a font template's black pixels aren't within a certain range of the segment, the XOR comparison is skipped.


###Final Thoughts

Using templates can be successful. But when the input data varies greatly from the training data it doesn’t work very well. One of the biggest limitations of my program is that it uses a single sans-serif alphabet for the OCR comparison and requires white space between glyphs for segmentation. If an input image varies greatly from this alphabet, character recognition is flawed, which ultimately affects the font match. 

In the next iteration, I'm interesed in using topological feature analysis to classify letters. By reducing a character to its most basic structure (i.e., open areas, closed shapes, diagonal lines) the input glyph could then be compared against these measurements and classified accordingly. Incorporating a feature that allows the program to learn from user feedback would also improve the OCR match. 

I'd also like to expand the range of quality of the images that can be processed. I plan to do this by improving thresholding and introducing noise reduction and skew detection. 





