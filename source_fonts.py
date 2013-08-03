import os
import csv
import urllib

### will need to incorporate into seed.py after testing 
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
	
	
	font_dict = {}
	# [0:51]:
	for url in font_urls:
		# rename downloaded file to 'font_name.ttf'
		name = url.split("=")[-1] 
		name = name.strip(',')
		name += '.ttf'
		font_dict.setdefault(name, url)

		# urllib.urlretrieve(url, os.path.join(path, name))
	return font_dict

def write_fonts_to_master(font_dict, myfile):

	with open(myfile, 'wb') as f:  
		w = csv.writer(f)
		w.writerows(font_dict.items())		


def main():
	
	file_url = 'font/font/file'
	font_urls = source_data(file_url) 
	font_dict = download_fonts(font_urls)
	myfile = 'master_fonts.csv'
	write_fonts_to_master(font_dict, myfile)
	




if __name__== "__main__":
	main()


