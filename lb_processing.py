from flask import jsonify
from scraper import scrawl_user_reviews
from cloud import create_wordcloud
from os import path
# import app
import tempfile
from base64 import b64encode


def cloud_processing(username):
	with tempfile.TemporaryDirectory() as tempdir:
		create_wordcloud(" ".join(scrawl_user_reviews(username)), username, tempdir)
		image_file = path.join(tempdir, f"{username}.png")
		with open(image_file, 'rb') as img:
			image_binary = img.read()
			image = b64encode(image_binary).decode("utf-8")
			return image