from wordcloud import WordCloud, STOPWORDS
from PIL import Image
import numpy as np
from os import path


def create_wordcloud(text, name, tempdir):
	currdir = path.dirname(__file__)
	mask = np.array(Image.open(path.join(currdir, "static/cloud_wide.png")))
	stopwords = set(STOPWORDS)
	wc = WordCloud(background_color="#F9F9F9",
					max_words=200, 
					mask=mask,
	               	stopwords=stopwords)
	wc.generate(text)
	wc.to_file(path.join(tempdir, f"{name}.png"))
