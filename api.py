import os
import json
import urllib

from flask import Flask, jsonify, request, url_for, redirect, render_template
from werkzeug import secure_filename

import model
import ranked_match
import get_segments



# UPLOAD_FOLDER = '/user_images'
# # where uploaded files will be stored
# ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png', 'gif'])
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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
		# have to escape slashes  
		segments = get_segments.main(img_url)
		result = json.dumps(segments)
		

	except IOError:
		message = "Oh, snap. I can't find that image. Can you try a different image?"
		return json.dumps(message) 

	if result:
		return redirect(url_for('match_font'))
	
	# http%3A%2F%2Fwww.flickr.com%2Fphotos%2graciferwong%29466743943%2F 
	# hello_world.jpg:http://www.flickr.com/photos/graciferwong/9466743943/
	# fox_novocento.png: http://www.flickr.com/photos/graciferwong/9466743485/
	#graceserver.com/send_image?img=http%40%30%30hackbright%16com%30hello%16jpg
	# googleimg: http%3A%2F%2Fwww.google.com%2Fimages%2Fsrpr%2Flogo4w.png
	
@app.route ('/match_font', methods = ['GET'])
def match_font():
	my_font = ranked_match.main()
	result = json.dumps(my_font)
	return result 

@app.route ('/')
def home():
	return render_template('index.html')

@app.route ('/index', methods = ['GET'])
def index():
	message = "Welcome to FontSeeker"
	result = json.dumps(message)
	return result 


if __name__ == '__main__':
	app.run(debug = True)

