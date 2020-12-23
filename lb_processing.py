from flask import jsonify
from scraper import scrawl_user_reviews, validate_user
from cloud import create_wordcloud
from os import path
import tempfile
from base64 import b64encode


def cloud_processing(username):
	if not validate_user(username):
		return False
	with tempfile.TemporaryDirectory() as tempdir:
		create_wordcloud(" ".join(scrawl_user_reviews(username)), username, tempdir)
		image_file = path.join(tempdir, f"{username}.png")
		with open(image_file, 'rb') as img:
			image_binary = img.read()
			image = b64encode(image_binary).decode("utf-8")
			return image