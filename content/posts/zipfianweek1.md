title: Zipfian Academy Weekly log: Accelerated Learning
date: 2013-09-22
tags: zipfian academy
author: Motoki Wu
summary: the first cohort

*This is my weekly diary of my experience at [Zipfian Academy](http://zipfianacademy.com/), a one of a kind data science bootcamp. I will have an ultimate review on this experience once my job search is complete.*

[Week 1](#week1), [Week 2](#week2), [Week 3](#week3), [Week 4](#week4), [Week 5](#week5), [Week 6](#week6)

## <a id="week1"></a>Week 1: you should bring a Mac

### Techniques learned: UNIX scripting, git, Python (functional programming, Beautiful Soup, IPython Notebooks, Numpy)

### Topics covered: source control, stdin stdout, unit testing, debugging, text parsing, collaborative filter recommender

It felt good to finally be busy again after a period of inactivity. It was finally time for 12 hours a day of coding and learning topics that barely register at Universities. After our meet and greet, we installed [Vagrant](http://www.vagrantup.com) in our machines in order to use a well-stocked virtual environment. A couple of non-Mac people experienced some trouble setting up the virtual environment, but such is life for making disparate software work together.

The day generally goes like this: 

* **0830~0930** | Tightening previous day's work
* **0930~1030** | Code review and lecture on concepts 
* **1030~1300** | Cooode
* **1300~1430** | Nominally lunch, realistically cooode
* **1430~1530** | Code review and lecture for the code sprint
* **1530~1800** | Code sprint so cooode
* **1800~????** | Usually two more hours of fixing stuff or doing extra material

The work is fairly hard and there is a lot of stuff to learn, but it never feels like it's too much. Coding along with other smart people caged in one room is stimulating and it never gets boring. Instructors and mentors are always available to help us focus in the right direction. [Jon](https://twitter.com/clearspandex) is especially gifted at explaining concepts from general principles and makes absolutely sure that we do not become slaves to the tools. 

**Self-teaching is O(n^2)**

The first week was focused on processing text with common UNIX tools, getting used to the Git flow and building an Amazon recommender in Python. I could say more, but I'd like to focus on Python for now.

As an R person, I always wanted to learn Python. I've heard a lot of good things from leaner memory management to faster routines and even its [data.frame capabilities](http://pandas.pydata.org/index.html). But I just never got along to it, as R's vast library and my familiarity with the language prevented me from jumping ship. I actually forced myself to learn Python about a month ago just because it seemed like the de facto language of data scientists (I only recently became interested in data science). 

Maybe I'm lazy and slow, but in two days I learned more at Zipfian than I self-taught in a month. I now know data types (sets, dicts, etc.), classes (self, scoping, etc.), modules (BeautifulSoup, NumPy), functional programming (map(), reduce(), list comps, etc.), IPython notebooks, unit tests, debugging, file I/O, etc. I do not have deep knowledge behind the algorithms and the models as someone who has years of experience, but I already have a strong enough base to know where to look if I don't know something. The idea is to get 80% familiar with a technique and take it from there. 

Easily the most beneficial characteristic of this learning experience is that the instructors put data science techniques *in context* such that you'll know which skills to apply in what situations. You can easily get inundated with online resources that can cause paralysis during self-study. 

<!-- there are certainly people that are behind, one is way ahead so he's just doing a personal project: living in sf lots of activities, more networking and events than i though: zipfian first 5 weeks, fundamentals teaching while coding, 2.5% chance of going in, 13 peeps, univ vs  accelerated learning -->

## <a id="week2"></a>Week 2: naive Bayesian learning

### Techniques learned: Python (matplotlib, pymc, pandas), processing.org, D3

### Topics covered: high level Bayesian and frequentist statistics, recursion (linked list, trees), algorithmic efficiency, object oriented programming, A/B testing

This week we went deeper into Python OO principles (classes, subclasses, scoping, instances, inheritance, etc.), packages for analytics (mainly NumPy, SciPy, pandas, and PyMC) and visualizations (D3, matplotlib and [processing](http://processing.org/)). We also talked a bit on data structures and algorithmic efficiencies (more for job interviews). 

We touched Bayesian statistics, MCMC and frequentist hypothesis testing in basically one day. As a person who studied statistics in college (plus two years of graduate-level stats), it confirmed how impossible it is to learn all of this stuff in a compressed fashion. It was a breeze for me (PyMC for example is **really** similar to WinBUGS / JAGS), but I can only imagine that it was a blur for people who haven't been exposed to deeper statistics. Similar to a work environment, practical skills can be learned very quickly where you're working on tangible projects with real deadlines; but broad based learning is more well-suited to a simmering schedule. Computer science fundamentals are something that I have to study up on.

## <a id="week3"></a>Week 3: San Francisco is Silicon Valley

### Techniques learned: scikit-learn, MongoDB

### Topics covered: high level machine learning, NoSQL databases, web scraping, natural language processing, regular expressions

Much of this week was occupied by [DataWeek](http://dataweek.co/). There wasn't much instruction except for the machine learning workshop on Monday. It was supposed to be a mini-bootcamp that the Zipfian fellows and conference attendees would participate in union. But technical problems ensued (we were not going to install [Anaconda](https://store.continuum.io/cshop/anaconda/) and a 150MB dataset to run a few [scikit-learn](http://scikit-learn.org/stable/) models on a paltry WiFi connection in a room of 80 nerds), so it morphed into a long lecture. 

Tuesday was catch up day for half of the cohort. People that were ahead started on their blogs, I started a mini data science project that I am hoping to finish soon. We roamed around Fort Mason on Wednesday and Thursday to attend talks at DataWeek. The talks broke down as follows: 3 parts data engineering, 3 parts how to leverage big data for business, 3 parts data APIs and 1 part science (at best). I was most interested in the science so the talks left me wanting. The overall vibe that I got was that San Francisco is *the* epicenter for data entrepreneurship. 

Friday was more like a programming bootcamp. A whirlwind tour through MongoDB and [Wikipedia API](http://www.mediawiki.org/wiki/API:Main_page). 

## <a id="week4"></a>Week 4: Hadoop makes easy problems hard, hard problems possible, while SQL is just a PITA

### Techniques learned: SQLite, Hadoop streaming, MapReduce

### Topics covered: relational databases, naive Bayes, overfitting, supervised learning, classification, feature engineering, cross-validation

I think I found my achilles heel. It turns out it's databases. I've been going through the work and I'm usually one of the fast ones. For the SQL work however, I got behind for the first time. What's kind of neat about this bootcamp is that we all come from diverse backgrounds. So there is a fair amount of disparity in how fast people grasp the material. This time, I was on the short end of the stick relatively speaking, where weeks 2 and 3 were smooth sailing. The deal with SQL is that I tend to write terse code; and that is a no-no when you need to keep the data relational.

This week was surely the hardest of the weeks, as more and more difficult concepts get introduced in progressive fashion. In week 1, exercises were more structured and precise answers were required via unit tests. Now we do cross-validation where it is a sensitivity analysis free for all. The naive Bayes classifier was implemented in three different ways: Python, SQL and Hadoop streaming. This simulates scaling up data to petabyte-scale to experience the tradeoffs in programming ease vs. sheer horsepower. 

[Ryan](https://twitter.com/ryanorban) blazed through some exciting developments in big data computing. Traditionally, an abstraction layer like (SQL-ish Hive to more functional Pig) on top of Hadoop MapReduce. Directly accessing the Hadoop shell is of course possible, but generally not recommended for more complicated task (Java is not dynamic enough). Hadoop is well-tested for distributed computing and easy to speed up big computations linearly (just add rackunits). But [there are shortcomings](http://gigaom.com/2012/07/07/why-the-days-are-numbered-for-hadoop-as-we-know-it/) like constantly saving data to HDFS and being limited to MapReduce. There is tremendous competition to provide a better interface to Hadoop ([Dremel and Impala](http://www.quora.com/Cloudera-Impala/How-does-Clouderas-Impala-compare-to-Googles-Dremel)) or to provide a realtime processing alternative ([Spark](http://spark.incubator.apache.org/)).

Speaking of big data, the data science analytics team at Facebook came to Zipfian and talk to us about what goes on at Facebook. Facebook is currently hiring data scientists like crazy (ten a month). They are now at 90 data scientists but they say that due to the nature of the (petabyte-level social network) data, only small teams are working on each problem (graph search was supposedly one data scientist plus some engineers). All of the data engineering crap is taken care of, which is something to keep in mind for people who want to work mainly in analytics.

## <a id="week5"></a>Week 5: 

### Techniques learned: scikit-learn, Flask, Amazon EC2, ggplot2

### Topics covered: hierarchical clustering, k-means clustering, non-matrix factorization, grammar of graphics, RESTful web API

This week, we coded up unsupervised learning algorithms. We compared them against scikit-learn implementations and were shocked at how slow our implementations were. Slow is one thing (not enough FORTRAN), but scikit-learn separates the vectorization, model formulation and fitting. Along with duck typing, this creates very readable code. 

For example, here are the steps to calculate the multinomial Naive Bayes classifier (ignoring the prior):

1. Count the number of each feature with a label.
2. Divide 1. with the number of total features within a label.
3. Sum the log of each of these probabilities.
4. Get the arg max for the classification.

How I naively code up these steps is to serialize the code. I will have code for each step, and will run it one by one. I might construct a class and call a method at each step. If I want to run another model, fit a different vectorizer, even a random forests algorithm, the code length will just blow up. 
	
Alternatively, a minimal scikit-learn process would look like this:

	:::python
	## load data
	data = json.load(open("articles_html1000.json"))
	labels = map(lambda x: x['section_name'], data)

	## set vectorizer and count each word (feature)
	vectorizer = feature_extraction.text.CountVectorizer(min_df = 1)
	X = vectorizer.fit_transform(data)

	## set and fit model
	model = naive_bayes.MultinomialNB()
	model.fit(X, labels)
	
Not only does is it clear what we're doing, it is easy to swap out models, vectorizations and / or prediction methods. Including new data is seamless as you can insert them into the same vectorizer while predicting with the same model and model fit. 

	:::python
	## new data
	x_new = vectorizer.transform(newdata)
	model.predict(x_new)[0]

Cross-validation is built-in, and model checking is very fast. In R, you'll most likely have different packages with disparate syntax making it hard to do model comparison.

<b>Refs</b>

1. [API design for machine learning software: experiences from the scikit-learn project](http://arxiv.org/abs/1309.0238)

## <a id="week6"></a>Week 6: 

### Techniques learned: more scikit-learn, D3

### Topics covered: decision trees, random forests, gradient descent, linear regression, DOM

projects