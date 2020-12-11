from flask import Flask, render_template, url_for, flash, request, send_file, jsonify
import io
from scraper import scrawl_user_reviews
from cloud import create_wordcloud
from os import path
import tempfile
from base64 import b64encode


app = Flask(__name__)

app.config['SECRET_KEY'] = '%vbrv5cngh=^k_cjjj+1ruw+0c-5i(pn$zm)3o8sjpv_st8u3v';


@app.route("/", methods=['GET', 'POST'])
def home():
	image_file = None
	return render_template("home.html", image_file=image_file)


@app.route("/get-cloud", methods=['POST'])
def get_cloud():
	username = request.form['username']
	if username:
		with tempfile.TemporaryDirectory() as tempdir:
			create_wordcloud(" ".join(scrawl_user_reviews(username)), username, tempdir)
			image_file = path.join(tempdir, f"{username}.png")
			with open(image_file, 'rb') as img:
				image_binary = img.read()
				image = b64encode(image_binary).decode("utf-8")
				return jsonify({'status': True, 'image': image})
	return jsonify({'error': 'Missing data'})


if __name__ == '__main__':
    app.run(debug=True)