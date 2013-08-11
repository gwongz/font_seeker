import os, json, urllib
from flask import Flask, jsonify, request, url_for, redirect
from werkzeug import secure_filename
import model
import match_letter
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
		imgname = request.args.get('img')
		# has to be passed in without 
		segments = get_segments.main(imgname)
		result = json.dumps(segments)
		return result 

	except IOError:
		message = "I can't find that image. Did you remember to encode your url?"
		return json.dumps(message) 

	
	# http%3A%2F%2Fwww.flickr.com%2Fphotos%2graciferwong%29466743943%2F 
	# hello_world.jpg:http://www.flickr.com/photos/graciferwong/9466743943/
	# fox_novocento.png: http://www.flickr.com/photos/graciferwong/9466743485/
	#graceserver.com/send_image?img=http%40%30%30hackbright%16com%30hello%16jpg
	# googleimg: http%3A%2F%2Fwww.google.com%2Fimages%2Fsrpr%2Flogo4w.png
	
@app.route ('/match_font', methods = ['GET'])
def match_font():
	my_font = match_letter.main()
	result = json.dumps(my_font)
	return result 

@app.route ('/index', methods = ['GET'])
def index():
	message = "Welcome to font match."
	result = json.dumps(message)
	return result 

if __name__ == '__main__':
	app.run(debug = True)

