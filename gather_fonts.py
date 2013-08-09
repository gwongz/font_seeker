import re, csv, urllib, os
import zipfile
import StringIO
from PIL import Image, ImageDraw, ImageFont
import requests


def get_font_names(inputfile, myfile):

	f = open(inputfile)
	content = f.read()
	f.close()
	# pattern = re.compile('[family_name":\w*]', content)
	
	pattern = '"family_name":\w+'
	matches = re.findall('"family_name":"\w*"', content)
	root = 'http://www.fontsquirrel.com/fontfacekit/'

	clean_matches = []

	for match in matches:
		match = match.split('":"')
		match = match[1].strip('"')
		clean_matches.append(root+match)

	
	with open(myfile, 'wb') as outfile:  
		w = csv.writer(outfile)
		w.writerow(clean_matches)

	print clean_matches

def get_fonts():

	f = open('fs_sans_serif')
	font_urls = f.read()
	font_urls = font_urls.split(',')
	return font_urls 

	# with open('fs_sans_serif') as csvfile:
	# 	font_urls = csv.reader(csvfile, delimiter = ',')
	# 	for row in font_urls:
	# 		download = download_zipped_fonts(row)
		# 	download_zipped_fonts(url)

	

def download_zipped_fonts(font_urls):

	os.chdir('fontsquirrel')	

	for url in font_urls:
		try:
		
			r = requests.get(url)
			z = zipfile.ZipFile(StringIO.StringIO(r.content))	
			z.extractall()
			print r.ok
	
		except(zipfile.BadZipfile, zipfile.LargeZipFile), e:
        	
        	print "There was a bad file: %s" % (z)
        	continue 


def main():

	fonts = get_font_names('fs_sans_serif_dump.txt', 'fs_sans_serif')	
	font_urls = get_fonts()
	download_zipped_fonts(font_urls)


if __name__== "__main__":
	main()
