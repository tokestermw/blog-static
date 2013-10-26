title: A Simple Flask App to Classify New York Times Articles on Amazon EC2
date: 2013-10-25
tags: flask, scikit-learn, python
author: Motoki Wu
summary: my useless app store

Making apps was not on my radar before I started [Zipfian Academy](https://twitter.com/ZipfianAcademy), but I've been more and more convinced that data visualizations and interactive apps are essential skills of a data scientist. Even if I have the best predictive model in the world and tables that show it outperforms other models, but if those results are not digestible by the public, it's meaningless. As much data science is about good analysis and getting good data, it's also about messaging and providing a service for the client and the public. 

So I created a fairly simple [Flask app](http://flask.pocoo.org/docs/api/) that takes a corpus of New York Times articles to classify with respect to category (e.g. Technology). 

1. Scrape a bunch of NYT article, tokenize, stitch them together to create a corpus.
2. Label each NYT article (e.g. Technology).
3. Fit a Naive Bayes Classifier that predicts the label using new text.
4. Use Flask to let users explore model results by inserting a NYT URL on [Amazon EC2](http://aws.amazon.com/console/). 

You can check out the app at either of the links. Enter a valid NYT URL and it will figure out the label (i.e. the real category) by tokenizing the HTML and it predicts the label using only the text. The model is already fit and pickled, so I just have to upload it.

![test amazon](|filename|/images/test-amazon-nyt.png)

[http://ec2-54-200-81-28.us-west-2.compute.amazonaws.com:10080/](http://ec2-54-200-81-28.us-west-2.compute.amazonaws.com:10080/)

[http://ubuntu@54.200.81.28:10080](http://ubuntu@54.200.81.28:10080)

Some notes on the code. 

1. The decorator ```@app.route``` does all the work so when you hit a certain URL, it runs the decorated function.
2. I have a global ```OUTPUT``` variable to keep track of each predictions. ```OUTPUT``` is refreshed each time you hit the index page.
3. In my [Jinja2 template](http://jinja.pocoo.org/docs/) file, I have a for loop that loops over ```OUTPUT``` to show the results of the model.
4. I changed the ```logging.basicConfig``` to stream Python errors instead of the GET and POST requests.
5. ```run_model()``` loads the fitted model, gets the new text and label, then predicts.
6. I turn ```app.debug``` false and ```host='0.0.0.0'``` when hosting it on Amazon. 

I also use [screen](http://kb.iu.edu/data/acuy.html) to have the app constantly running. 

	:::python
	from flask import Flask, render_template, request, redirect, url_for, abort, session

	from sklearn import naive_bayes, feature_extraction, cross_validation
	from sklearn.externals import joblib
	import requests
	from bs4 import BeautifulSoup

	# make sure to show Python errors during debugging
	import sys, logging
	logging.basicConfig(stream = sys.stderr)

	app = Flask(__name__)

	@app.route('/')
	@app.route('/index.html')
	def hello():
		global OUTPUT
		OUTPUT = []
		return render_template("index.html", 
			SITENAME = 'Naive Bayes Classifier on a corpus of NYT Articles', 
			AUTHOR = 'Motoki Wu')

	@app.route('/results', methods = ['GET'])
	def splash():
		return render_template("index.html")

	@app.route('/results', methods=['POST'])
	def people_search():
		url = request.form.get('search')
		new_label, out = run_model(url)
		OUTPUT.append({'out':out, 'new_label':new_label})
		return render_template("result.html", output = OUTPUT,
			SITENAME = 'Naive Bayes Classifier on a corpus of NYT Articles', 
			AUTHOR = 'Motoki Wu')

	def run_model(url):
		model, vectorizer, X = joblib.load("model.pkl")
		new_article = requests.get(url)
		html = new_article.text
		soup = BeautifulSoup(html)
		div = soup.find_all("div", "articleBody")
		text = '\n'.join([str(i) for i in div])
		new_label = soup('meta', {'itemprop':'articleSection'})[0]['content']
		x_new = vectorizer.transform([text])
		out = model.predict(x_new)[0]
		return new_label, out

	if __name__ == '__main__':
		app.debug = True
		app.run()

	# for amazon
	# app.run(host='0.0.0.0', port=10080)

This is only one of many different ways to set up an app. You can easily swap out different classifiers, corpora or performance metric. A different app can take single or multiple NYT articles, or even non-NYT article text. It can perform different cross-validation a priori and let the user pick various tuned classifiers from a drop down menu. More sophisticated apps may include ensemble estimates and visualizations of performance statistics. 
