Installation notes:

Install SimpleCV from source
Brew install OpenCV
PIP install PIL, numpy, scipy
Install pygame from source 

To test get_segments.py, run the script from the command line followed by an imgfile 

Match_letter.py takes cropped segment and performs xor match against templates of each letter in the alphabet to identify which letter of the alphabet it is.

Draw_samples.py draws A-Z and a-z samples of each font and stores in local directory.

Model.py creates schema for sqlite3 database. Seed.py loads font samples into fonts.db database.

