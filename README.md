<h2>Installation notes:</h2>

Install SimpleCV from source<br>
Brew install OpenCV<br>
PIP install PIL, numpy, scipy<br>
Install pygame from source <br>

<h2>Overview:</h2>
Have you ever walked by a poster or sign and wanted to know what font the designer used? That happens to me a lot and it’s how this project came to be. FontSeeker was envisoned to be a Shazam for font identification. It takes an image, segments it into glyphs and uses a template-based approach to make a match against a database of font samples (currently just over 100) collected from Font Squirrel and fonts I already owned. FontSeeker was built with Python, Flask, PIL, SimpleCV and SQLAlchemy and uses AJAX on the front end. 

<h2>File Tree:</h2>
- draw_fonts.py: Uses PIL to draw lowercase and uppercase templates of each font, the OCR alphabet and specimen messages to return to user upon successful match.<br>
- process_images.py: Uses SimpleCV to crop an image to bounds and resize it to a fixed size while maintaining its aspect ratio.<br>
- model.py and seed.py: Creates schema for database and loads fonts, font templates and OCR training letters into database.<br>
-get_segments.py: Converts an image into a binary image and crops the image in locations where all-white columns are identified.<br>
- ranked_match.py: Segmented user images are compared against OCR alphabet and given a letter classification. Each segment is then compared against all the fonts for that letter classification. If the XOR difference meets a certain threshold, it is added to a font table. Fonts are then ranked based on the lowest average XOR difference and frequency of matches made.

<h2>Template-based Approach</h2>

Imaging libraries such as SimpleCV have powerful tools for extracting features from images, but I hadn’t worked with images before so I decided to start with basic template matching — the most straightforward approach to symbol recognition. 

Since an image can be converted to a 2D array of black and white pixels, character and font recognition can be made by performing a pixel-by-pixel comparison between input glyphs and template glyphs once segmentation has occurred. 

Template matching, however, is a slow process. The matching program I wrote has a Big O time of 2 O(n^2) which is far from ideal. I refactored the code to speed up the run time - comparing each segment to OCR and then to the font and breaking out of the loop once a certain font had been matched at least n times - but this sacrificed matching accuracy. 

To get the best OCR match, I decided that a full pass through the alphabet was needed. Once that decision was made, optimization efforts were focused on how to reduce wasteful matches during font comparison. To improve run time, I refactored the code to:

- throw out segments which had a low OCR XOR difference value above 0.2
- skip font matches when the letter is likely to cause more errors than its removal would (e.g., segments identified as a “I, i, or l”)
- process more image data before matching occurs. The number of black pixels in each template image can be calculated and loaded in the database before the match process begins. That way, if a font template’s black pixels aren’t within a certain range of the segment, the XOR comparison is skipped.


<h2>Final Thoughts:</h2>

Using templates to make a match is a straightforward approach and can be successful. But when the input data varies greatly from the training data it doesn’t work very well. One of the biggest limitations of my program is that it only uses one sans-serif alphabet for the OCR comparison and requires white space between glyphs for segmentation. 

If an input image varies greatly from this alphabet, character recognition is flawed, which ultimately affects the font match. In the next stage, I could train the OCR with more alphabets or use a OCR engine like Tesseract or OCRopus. But character recognition is ultimately something that humans are much better at than computers, which makes me think that for font matching purposes, it would be more efficient to have the user input the letters to be compared when they submit their image.

When it comes to font matching, in my next iteration I’d like to take a statistical approach, which would improve processing time and be more robust when it comes to making matches. By extracting additional features such as aspect ratio and area, it would be possible to break down an image into a simple signature. Then the input glyph could be compared against these measurements and classified accordingly. 




