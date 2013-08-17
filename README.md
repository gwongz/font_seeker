Installation notes:

Install SimpleCV from source<p>
Brew install OpenCV<p>
PIP install PIL, numpy, scipy<p>
Install pygame from source <p>

FontSeeker is a tool that identifies the font used in an image file. It uses segmentation, OCR and XOR comparison to match the segments against a database of font samples. FontSeeker was built with Python, Flask, PIL, SimpleCV and SQLAlchemy and uses AJAX on the front end. The database is seeded with fonts collected using the FontSquirrel API. <p></p>

Seeding and modeling the database:
Source_fonts.py is a script that downloads font files from the FontSquirrel API. Draw_fonts.py uses PIL to draw lowercase and uppercase templates of each font and to draw an OCR alphabet.  
Model.py creates the schema for the database and seed.py loads the font templates and OCR templates into the database.

Image processing:
Process_images uses SimpleCV to crop an image to bounds and resize it to a fixed size while maintaining its aspect ratio. 
Get_segments converts an image into a binary file, attempts to identify white space between text and crops the image at those bounds. The segments are then cropped to bounds and resized. 

Ranked_match:
OCR is performed against the segments created by get_segments. An XOR comparison is made between each segment and OCR alphabet and a letter is identified for each segment. Then each segmented letter is compared against all the font samples for that letter in the database. If the XOR difference meets a certain threshold, it is added to a font table. At the end of the process, the fonts are ranked based on the lowest average XOR difference and frequency of matches.

Run time and optimization:
The matching has a Big O time of 2 O(n^2) which isn’t ideal. I refactored the code to a O(n^3) — comparing each segment to OCR and then to the font and breaking out of the loop once a certain font had been matched at least n times -- but this sacrificed matching accuracy.



