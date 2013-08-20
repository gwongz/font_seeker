FontSeeker
==========

Have you ever walked by a poster or sign and wanted to know what font the designer used? FontSeeker was envisoned to be a Shazam for font identification. It takes an image, segments it into glyphs and uses a template-based approach to make a match against a database of font samples (currently just over 100) collected from Font Squirrel and fonts I already owned. FontSeeker was built with Python, Flask, PIL, SimpleCV and SQLAlchemy and uses AJAX on the front end. 


###Segmentation
#####(get_segments.py)
Converts an image into a binary image and crops the image in locations where all-white columns are identified.

###OCR and Font Match
#####(ranked_match.py)
Segmented glyphs are compared against the OCR alphabet and given a letter classification. Each segment is then compared against all the fonts for that letter classification. If the XOR difference meets a certain threshold, it is added to a font table. Fonts are then ranked based on the lowest average XOR difference.

###Load Fonts and Database
######(draw_fonts.py, model.py, seed.py)
PIL is used to draw lowercase and uppercase templates for fonts collected from the FontSquirrel API. An OCR alphabet and specimen messages are also drawn from font files. The database is seeded using Python and SQLAlchemy. <br>

###Image Processing
#####(process_images.py)
SimpleCV is used to crop an image to bounds and resize it to a fixed size while maintaining its aspect ratio.

###Web Framework
######(main.py)
Flask is used for the web framework. AJAX is used to send the user's image to the server and call the route that returns the closest matched font in JSON.
The front end uses HTML5 and CSS.

![Alt text](/screenshots/fontseeker.png "Screenshot of sample results")




 





