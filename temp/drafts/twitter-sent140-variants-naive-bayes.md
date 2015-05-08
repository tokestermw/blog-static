title: Twitter #BartStrike Data: Sentiment Analysis with Distant Supervision
date: 2014-04-19
tags: python, scikit-learn, nlp
author: Motoki Wu
summary: maybe

I am a frequent user of public transportation (of what's there) in the San Francisco Bay Area. BART (Bay Area Rapid Transit) is a regional rail service that connects the Bay Area suburbs with many large cities. Late last year, there was a [BART strike(s)](http://www.mapreport.com/na/west/ba/news/cities/bart_strike.html) that caused an uproar since it caused commuters to look for alternatives even when the commute is crowded as is. I was affected, so I kept my finger on the pulse for updates of the dispute; this was also the time I started Twitter. The upside of the strike was I got to ride on the ferry and collect data on the BART strike. 

I used the [Twitter Streaming API](https://dev.twitter.com/docs/api/streaming) to get tweets of the #BARTstrike hashtag as much as I was allowed to. The time period that was streamed was from the second BART strike to the end of it -- about a week. In total, I got an original dataset of about 13000 tweets to play with. Other folks have worked on the BART strike too, namely: [Hack the BART Strike](https://github.com/enjalot/bart). 

### Data Summary

The easiest thing to look at first the counts. I used [tm package in R](http://www.rdatamining.com/examples/text-mining) to do most of the lifting (tokenization, stop words, punctuation, etc.; couldn't stem for some reason). I use R since I don't trust Matplotlib with the visualizations. Though creating the term frequency matrix blew up the R process to take up 3 GB of memory but I digress. Below is the word cloud of most common words in the tweets.

![image](|filename|/images/wordcloud.png)

One thing you'll notice is that a lot of the words are related to methods of transportation ("trains", "home ride", "buses", "service", "#carpool"). [Carma](https://carmacarpool.com) has a carpooling app so they were enthusiastically tweeting about their service. The other words seems to be directed *at* the transit workers ("union", "workers", "support", "#dearbart"). [@atu_1555](https://twitter.com/ATU_1555) is the Twitter account for the transit union and [@sfbart](https://twitter.com/SFBART) is the official account for BART. Surprisingly, I didn't see many negative words associated with the highest word counts.

### Emojis

I wanted to know the most influential words in determining positive or negative sentiment of these tweets. The easiest is to do supervised learning, but it is the labor-intensive to label the data. 

I am too lazy to hand-label (also surprisingly difficult to assess sentiment once I actually tried it; tons of edge cases) so I looked at [distant supervision (Go et al. 2009)](http://s3.eddieoz.com/docs/sentiment_analysis/Twitter_Sentiment_Classification_using_Distant_Supervision.pdf). The basic idea is to use fairly definitive features as a proxy for labeling sentiment -- for example, emojis (emoticons). A ':)' indicates a high likelihood of positive sentiment so any tweets that has a smiley would be labelled as positive. After stripping out all the emojis used for labeling, I can use a supervised learning algorithm assess sentiment. 

I actually didn't use this method since my regexp-fu wasn't enough to amount to a substantial dataset. What I had left was still interesting. Here is a moving average of emoji sentiment over the course of the week:

![image](|filename|/images/emoticon.png)

### Supervised Learning

Lazily, I used the [Sentiment140](http://help.sentiment140.com/api) to label the data. Sentiment140 is a classifier based on the Go et al. (2009) distant supervision method linked above. They train on 1,600,000 balanced set of tweets (positive, negative though no neutral class). I sent my data through their API, which takes a set of tweets and adds polarity (positive, neutral, negative). My guess is that they train a Naive Bayes (or SVM) with unigram features with negation (e.g. "not good"). 

I first took out the "neutral" class. Then I trained a Naive Bayes with binarized features, Naive Bayes with a TFIDF filter and a linear SVM through the new labelled dataset. The best model got me close 90% accuracy on the tweet sentiment. 

Here are the features with most negative sentiment:

	:::python
	>> display(imp_features[0:20])
	[(-2.8357465163165063, u"n't"),
	 (-2.4201593740395526, u'work'),
	 (-2.2099005503662612, u'sad'),
	 (-2.134341230708428, u'traffic'),
	 (-1.9487734183304863, u'bad'),
	 (-1.9410436588253621, u'suck'),
	 (-1.7625886379782472, u'hate'),
	 (-1.5710481225736643, u'still'),
	 (-1.5688234447934066, u'leaving'),
	 (-1.5295688143615913, u'stuck'),
	 (-1.5139701088397268, u'bus'),
	 (-1.5013235053943947, u'damn'),
	 (-1.4788029325321641, u'horrible'),
	 (-1.3002409121097998, u'missing'),
	 (-1.2643054498836144, u'stupid'),
	 (-1.2439906270740047, u'lost'),
	 (-1.2330823454521014, u'ugh'),
	 (-1.2300572586379617, u'missed'),
	 (-1.207876020758087, u'left'),
	 (-1.1925205756393427, u'sorry')]
 
 
 Here are the features with the most positive sentiment:
 
	:::python
	 >> display(imp_features[-21:-1])
	[(1.2572713812534602, u'abc7newsbayarea'),
	 (1.2848970173168219, u'nicely'),
	 (1.3114599170734345, u'yay'),
	 (1.3141989313725035, u'sfbayferry'),
	 (1.3331475843002596, u'ready'),
	 (1.3626098784763807, u'safe'),
	 (1.4427299291680631, u'awesome'),
	 (1.533406184356106, u'hey'),
	 (1.5904100695696874, u'thank'),
	 (1.6002919329257885, u'great'),
	 (1.6171697845738462, u'finally'),
	 (1.6259904844181883, u'sfbart'),
	 (1.6489921434356374, u'love'),
	 (1.6657530957108404, u'thx'),
	 (1.6724072807099553, u'best'),
	 (1.6875918587710637, u'excited'),
	 (1.728437377530184, u'good'),
	 (1.7847619469736122, u'nice'),
	 (2.2958159850061266, u'happy'),
	 (2.9483929041967141, u'http')]

There is obviously some double counting going on by using a classification algorithm to label the dataset and using a similar classification algorithm to predict the dataset. In the future, I'd like to expand on this analysis by running more complex algos. like [LDA](http://en.wikipedia.org/wiki/Latent_Dirichlet_allocation). 

### Refs
 
1. Go et al. (2009) [Twitter Sentiment Classification using Distant Supervision](http://s3.eddieoz.com/docs/sentiment_analysis/Twitter_Sentiment_Classification_using_Distant_Supervision.pdf). 
2. [Link to my IPython Notebook](http://nbviewer.ipython.org/github/tokestermw/twitter-bart/blob/master/ipynb/Twitter140-checkNB.ipynb)
3. [Link to my GitHub Repo](https://github.com/tokestermw/twitter-bart)
