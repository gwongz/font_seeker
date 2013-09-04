import os
import json
import urllib

from flask import Flask, jsonify, request, url_for, redirect, render_template
from werkzeug import secure_filename

import model
import ranked_match
import get_segments

app = Flask(__name__)
app.secret_key = 'dfkjdsf;adlkjf;ldkfj'

@app.route('/font_list', methods = ['GET'])
def get_all_fonts():

	fonts = model.session.query(model.Font.name).all()
	return jsonify(Fonts=fonts)

@app.route('/send_image', methods = ['GET'])
def send_image():

	try:
		img_url = request.args.get('img') 
		segments = get_segments.main(img_url)
	
		if segments == [] or len(segments) <= 1:
			result = None
		else:
			result = json.dumps(segments)
		
	except IOError:
		result = json.dumps(segments)

	return redirect(url_for('match_font'))



	
	
@app.route ('/match_font', methods = ['GET'])
def match_font():

	# returns list of strings
	my_font = ranked_match.main() 

	font_result = {}

	# no matches
	if my_font == []:
		font_result["success"] = False
	
	if len(my_font) >= 1: 
		font_result["success"] = True
		for item in my_font:
			font_result["font_name"] = item[0]
			font_result["difference_value"] = item[1]
			break

	result = json.dumps(font_result)
	return result 

@app.route ('/')
def home():
	return render_template('index.html')

@app.route ('/index', methods = ['GET'])
def index():
	return redirect(url_for('home'))


if __name__ == '__main__':
	app.run(debug = True)

