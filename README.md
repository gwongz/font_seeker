Font matching project for Hackbright using Python, sqlite3, and SimpleCV

Segments.py identifies white space in user submitted image and crops image into individual segments.

Xor.py takes cropped segment and performs xor match against templates of each letter in the alphabet to identify which letter of the alphabet it is.

Match.py will take cropped user image and perform xor match against all the fonts in database that match the identified letter.

Source_fonts.py loads font files collected from dafont into local directory. Draw_samples.py draws A-Z and a-z samples of each font and stores in local directory.

Model.py creates schema for sqlite3 database. Seed.py loads font samples into fonts.db database.

