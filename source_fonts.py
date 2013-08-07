import os
import csv
import urllib

"""Downloads font urls to local directory and creates csv file of fonts and urls"""


def source_data(file_url):

	with open (file_url) as csvfile:
		fonts = csv.reader(csvfile, delimiter=',', quotechar=',')
		font_urls = []
		# match = re.search(r'\Ahttp', fonts)
		for row in fonts:
			row = " ".join(row).strip(',')
			if 'http' not in row:
				continue
			else:
				font_urls.append(row)
		# a list of urls as strings
		return font_urls 


def download_fonts(font_urls):
	

	fontpath = 'templates'
	font_dict = {}
	# [0:51]:
	for url in font_urls[0:20]:
		# rename downloaded file to 'font_name.ttf'
		name = url.split("=")[-1] 
		name = name.strip(',')
		name += '.ttf'
		font_dict.setdefault(name, url)
		# downloads the file and saves it to the templates directory as '.ttf file'
		urllib.urlretrieve(url, os.path.join(fontpath, name))
	return font_dict

def write_fonts_to_master(font_dict, myfile):

	with open(myfile, 'wb') as f:  
		w = csv.writer(f)
		w.writerows(font_dict.items())		


def main():
	
	source_file = 'font/font/file'
	font_urls = source_data(source_file) 
	font_dict = download_fonts(font_urls)
	myfile = 'seed_data.csv'
	write_fonts_to_master(font_dict, myfile)


if __name__== "__main__":
	main()


