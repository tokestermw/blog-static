title: Yelp data challenge 2
date: 2013-12-07
tags: python, yelp, mongodb, random forests
author: Motoki Wu
summary: for a job

Yelp has a [dataset challenge](http://www.yelp.com/dataset_challenge/) that anyone can enter. I was given some questions to explore the dataset for an interview and wanted me to have a blog post. 

*Tell us about the day of week that people post reviews.*

1. *Are some days preferred?*
2. *Is there a correlation with categories?*
3. *Other interesting insights related to the day of week?*
4. *Any of them significant?*

The data consists of four JSON files (user, review, business, check-in). For the above questions, I only need to use the review data and the categories of the businesses. 

I first set up a MongoDB on my laptop then load all of the data into it.

	:::bash
	## import all of the data
	~/mongodb/bin/mongoimport --db yelpchallenge2 --collection business --type json --file yelp_academic_dataset_business.json
	~/mongodb/bin/mongoimport --db yelpchallenge2 --collection checkin --type json --file yelp_academic_dataset_checkin.json
	~/mongodb/bin/mongoimport --db yelpchallenge2 --collection review --type json --file yelp_academic_dataset_review.json
	~/mongodb/bin/mongoimport --db yelpchallenge2 --collection user --type json --file yelp_academic_dataset_user.json

Once MongoDB is running on the system, it is simple to connect it with Python.

	:::python
	from pymongo import MongoClient
	
	client = MongoClient()

	db = client['yelpchallenge2']

	c_biz = db['business']
	c_chk = db['checkin']
	c_rev = db['review']
	c_use = db['user']

To get a broad understanding of when people post their reviews, I first plotted the counts of the reviews for each weekday.

![bla](|filename|/images/weekday_hist.png)

People post most frequently on Mondays and then on Wednesdays. The test of independence says that people do not randomly post reviews on any day.

	:::python
	from scipy.stats import chisquare, kstest

	chisquare(obs, exp)
	# chi-squared statistic, p-value
	# (1207.6232302626715, 1.071911368415918e-257)

Looking at the review counts per month over time, people post more frequently on Sundays than before.

![bla](|filename|/images/weekday_ts.png)

Does the type of business matter when people post their reviews? To look at this, I first "joined" the business and reviews (Mongo) collections in order to grab the categories of the business for each review. 

	:::python
	bizid = [0] * c_rev.count()
	i = 0
	for rev in c_rev.find():
	    bizid[i] = rev['business_id']
	    i += 1

	cat = [0] * len(bizid)
	for i in xrange(len(bizid)):
	    # a Mongo join would be better (takes 10+ minutes)
	    # http://docs.mongodb.org/ecosystem/tutorial/model-data-for-ruby-on-rails/
	    cat[i] = c_biz.find_one({'business_id': bizid[i]})['categories']

In order to show relationships between business categories and weekdays, I first [binarized](http://scikit-learn.org/stable/modules/multiclass.html) the categories so I will have a binary column for each unique category. This will be helpful for the next section.

	:::python
	from sklearn.preprocessing import LabelBinarizer, LabelEncoder

	cat_set = list(set([i for sublist in cat for i in sublist]))
	cat2num = LabelEncoder().fit(cat_set)

	cat_num = [cat2num.transform(i) for i in cat]

	cat_bin = LabelBinarizer().fit_transform([list(i) for i in cat_num])

Then I plotted the distribution reviews for the weekdays for each category that has more than 1000 reviews (click to expand).

<a href="|filename|/images/pcolor.png" target="_blank">![bla](|filename|/images/pcolor.png)</a>

By looking at the heatmap, people post reviews on restaurants more frequently on Mondays. This might be an indication that people go out to eat on Sundays and then opine about their experiences on Mondays. The trend for "Bars," "Dive Bars" and "Barbeques" are even more extreme. The distributions for light meals in "Cafes" (also "Bagels", "Breakfast") are more heavily weighted towards Sundays. On the other hand, "Coffee" and "Japanese" have flat distributions. Some have a different shape like "Auto Repair," where people don't post anything on Sundays (closed?) but post (relatively) overwhelmingly on Wednesdays. That might be an indication that an average auto repair isn't finished by Monday. 

To predict the day of the week people post reviews by just using the categories, I run a multi-label classification. In a multi-label classification, every data point (*i.e.* review) has multiple labels (*i.e.* categories) that is impossible to model without any feature engineering. Broadly, there are two ways to go about this. One is data transformation (say picking one label out of multiple) and another is [algorithm adaption](http://www.sciencedirect.com/science/article/pii/S0031320312001203). 

To fit a classifier, I first binarized the multiple categories. Since that makes the matrix big and sparse, I subsetted the dataset so that only the categories with the highest counts (> 1000) remained. I don't consider correlation between labels ("Japanese" and "Sushi Bars" should be dependent) since that will blow up my memory. 

	:::python
	# subset
	indy = list(np.where(wd_cnt.sum(axis = 0) > 1000)[0])
	indx = list(np.where(cat_bin[:, indy].sum(axis = 1) > 0)[0])
	cat_sub = cat_bin[:, indy]
	cat_sub = cat_bin[indx, :]

I run a random forests classifier through the dataset and got back a 17.5% cross-validation score on itself. This is only +3% better than the null (1/7), but given the weak signal in the data itself, I don't think one can expect a huge improvement. Naive Bayes got me +2% better than the null. 

	clf = RandomForestClassifier(n_estimators = 100, n_jobs = 4)
	clf_fit = clf.fit(cat_sub, np.array(weekdays)[indx])

	scores = clf_fit.score(cat_sub, np.array(weekdays)[indx])
	# 0.17354151281780777

It's possible to run a PCA to do some meaningful dimensionality reduction, but I was more interested in what features were important. Random forests is nice because I can calculate which features were chosen to be higher in the set of trees.

Here are the feature importances from highest to lowest:

	:::python
	In [177]: sorted(clf_feat, key = clf_feat.get, reverse = True)
	Out[177]:
	[u'American (Traditional)',
	 u'Food',
	 u'Burgers',
	 u'Italian',
	 u'Shopping',
	 u'Event Planning & Services',
	 u'Breakfast & Brunch',
	 u'Pizza',
	 u'Sandwiches',
	 u'Coffee & Tea',
	 u'Restaurants',
	 u'Mexican',
	 u'American (New)',
	 u'Specialty Food',
	 u'Bakeries',
	 u'Active Life',
	 u'Arts & Entertainment',
	 u'Delis',
	 u'Beer, Wine & Spirits',
	 u'Fast Food',
	 u'Chinese',
	 u'Desserts',
	 u'Nightlife',
	 u'Vegetarian',
	 u'Grocery',
	 u'Asian Fusion',
	 u'Health & Medical',
	 u'Lounges',
	 u'Mediterranean',
	 u'Cafes',
	 u'Seafood',
	 u'Barbeque',
	 u'Buffets',
	 u'Sushi Bars',
	 u'Gluten-Free',
	 u'Sports Bars',
	 u'Bars',
	 u'Steakhouses',
	 u'Japanese',
	 u'Ice Cream & Frozen Yogurt',
	 u'Diners',
	 u'Wine Bars',
	 u'Hawaiian',
	 u'Home & Garden',
	 u'Hotels & Travel',
	 u'Pubs',
	 u'Vegan',
	 u'Hot Dogs',
	 u'Thai',
	 u'Fashion',
	 u'Automotive',
	 u'French',
	 u'Donuts',
	 u'Home Services',
	 u'Local Services',
	 u'Beauty & Spas',
	 u'Venues & Event Spaces',
	 u'Bagels',
	 u'Vietnamese',
	 u'Dive Bars',
	 u'Greek',
	 u'Music Venues',
	 u'Tex-Mex',
	 u'Breweries',
	 u'Day Spas',
	 u'Pets',
	 u'Shopping Centers',
	 u'Middle Eastern',
	 u'Fitness & Instruction',
	 u'Health Markets',
	 u'Southern',
	 u'Caribbean',
	 u'Cinema',
	 u'Latin American',
	 u"Women's Clothing",
	 u'Books, Mags, Music & Video',
	 u'Hotels',
	 u'Auto Repair',
	 u'Irish',
	 u'Parks',
	 u'Indian',
	 u'Gyms',
	 u'British',
	 u'Department Stores',
	 u'Nail Salons']

Again, the absolute differences are fairly small, but in general the restaurant reviews give the most signal in predicting when people post their reviews. I'm sure this is partly due to people using Yelp for restaurant reviews more than anything else (with "Shopping" and "Event Planning & Services" interspersed). Overall though, it's hard to parse out signal from a fairly uniformly distributed dataset.

Next steps:

1. Include correlation in the classifier
2. Dimensionality reduction
3. Use other data (ratings, review text)

The whole code is [posted in a gist](https://gist.github.com/tokestermw/7828738).