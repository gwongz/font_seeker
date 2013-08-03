import urllib
import os
import re
import csv
import re


def source_data(path):
	"""Returns list of urls from scraper csv file"""
	with open (path) as csvfile:
		fonts = csv.reader(csvfile, delimiter=',', quotechar=',')
		font_urls = []
		# match = re.search(r'\Ahttp', fonts)
		for row in fonts:
			row = " ".join(row).strip(',')
			if 'http' not in row:
				continue
			else:
				font_urls.append(row)
		return font_urls # list of strings
		# do I need to close this file?


def download_fonts(font_urls):
	"""Downloads ttf files from font urls -- 50 at a time and stores in local directory"""
	
	path = "font_files" # store in the font_files directory
	folder = ""
	names = []

	for url in font_urls[0:51]:
		# rename downloaded file to 'font_name.ttf'
		name = url.split("=")[-1] 
		name = name.strip(',')
		name += '.ttf'
		names.append(name)
		# urllib.urlretrieve(url, os.path.join(path, name))

def write_fonts_to_file(names, font_urls):
	for url in font_urls:
		url = url.split('=')[-1]

		


	master_fonts = open('master_fonts', 'wb')
	write = csv.writer(master_fonts, quoting=csv.QUOTE_ALL) # what does QUOTE_ALL do?
	write.writerow(url) # saves url and name to new csv file
	write.writerow(name)



	# open file and add list of font names and urls 


	# retrieves url and stores in font_files directory as name
	
	


I want to store in directory as "name"
I want to store in directory = "font_files" 

Do I want to store in appropriate letter
# I want to store it in /font_files
I want to store as cellos_script.ttf
# url = "http://img.dafont.com/dl/?f=cellos_script"

def main():
	
	path = 'font/font/file'
	fonts = source_data(path) # returns a list of strings
	print fonts 
	




if __name__== "__main__":
	main()


