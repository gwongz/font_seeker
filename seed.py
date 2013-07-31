"""Loads fonts from local directory into database"""

import model
import os.path 
import re 

from PIL import Image

os.path.join("path1", "path2", font)

def load_A (session):
	home = "/Users/gwongz/src/hackbright/project/font_files/A"
	font = "A.AppleGothic.png"
	path = os.path.join(home, font)
	
	with Image.open(path) as f:
		font = model.Letter_A(id = ord('A'),
							fontname = "AppleGothic",
							path = path)
		session.add(font)
	session.commit()



# filename = os.path.join('path', 'to', 'image', 'file')
# img = Image.open(filename)
# print img.size


def main(session):
	load_A(session)

if __name__ == "__main__":
	s = model.session
	main(s)
