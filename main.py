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
		result = json.dumps(segments)

	except IOError:
		message = "Oh, snap. I can't find that image. Can you try a different image?"
		return json.dumps(message) 

	if len(segments) <=1 or segments == []:
		return "I'm sorry, I'm not able to segment this image."
	else:
		return redirect(url_for('match_font'))


@app.route ('/match_font', methods = ['GET'])
def match_font():
	# returns list of strings
	my_font = ranked_match.main() 

	font_result = {}
	if len(my_font) >= 1: 
		font_result["success"] = True
		for item in my_font:
			font_result["font_name"] = item[0]
			font_result["difference_value"] = item[1]
			break

	if len(my_font) == 0:
		font_result["success"] = False
		font_result["multiple"] = False 

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