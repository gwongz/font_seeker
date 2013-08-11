import re, csv, urllib, os, shutil
import zipfile
import StringIO
from PIL import Image, ImageDraw, ImageFont
import requests

# use glob 


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

def make_font_urls():

	f = open('fs_sans_serif')
	font_urls = f.read()
	font_urls = font_urls.split(',')
	return font_urls 

	# with open('fs_sans_serif') as csvfile:
	# 	font_urls = csv.reader(csvfile, delimiter = ',')
	# 	for row in font_urls:
	# 		download = download_zipped_fonts(row)
		# 	download_zipped_fonts(url)

	

def download_zipped_fonts(font_urls, destdir):

	

	for url in font_urls:
		try:
			r = requests.get(url)
			z = zipfile.ZipFile(StringIO.StringIO(r.content))
			names = z.namelist()	

			ttfs = []

			for name in names:
				if '.ttf' in name:
					ttfs.append(name)

			for ttf in ttfs:
				z.extract(ttf, destdir)
			
			print r.ok

		except(zipfile.BadZipfile, zipfile.LargeZipFile), e:	
        		print "There was a bad file: %s" % (z)
        		continue 


def organize_fonts(srcdir, destdir):
	"Searches through fonts directory and reorganizes ttf files"
	if not os.path.exists(destdir):
		os.mkdir(destdir)

	for dirpath, dirnames, fnames in os.walk(srcdir):
		for f in fnames:
			if f.endswith ('.ttf'):
				pathname = os.path.join(dirpath, f)
				shutil.copy2(pathname, destdir)

	

	        	

def main():

	# fonts = get_font_names('fs_sans_serif_dump.txt', 'fs_sans_serif')	
	# font_urls = make_font_urls()
	# download_zipped_fonts(font_urls, 'fonts')
	# organize_fonts('fonts', 'font_files')
	


if __name__== "__main__":
	main()
