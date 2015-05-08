+++
title = "Visualization of Topic Models"
date = "2014-10-26"
tags = ["python", "topic modeling", "networkx", "gensim"]
+++

<blockquote class="twitter-tweet" lang="en"><p>Lies, damned lies and topic modeling.</p>&mdash; Motoki Wu (@plusepsilon) <a href="https://twitter.com/plusepsilon/status/526464306754240513">October 26, 2014</a></blockquote> <script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

There is still much work to do in interpreting and visualizing topic model word clusters so some tangible results can be derived in a research setting or something useful comes out in a production app. A cluster of words are likely to be noisy and illegible so I will be exploring a few options presented [here](http://tedunderwood.com/2012/11/11/visualizing-topic-models/) by [@Ted_Underwood](https://twitter.com/Ted_Underwood).
 
I took some Twitter data from [last year's BART strike](http://oaklandwiki.org/2013_BART_Strikes?&redirected_from=july%201st%202013%20strike) used in a previous [IPython notebook](http://nbviewer.ipython.org/github/tokestermw/twitter-bart/blob/master/ipynb/Twitter140-checkNB.ipynb). This data contains the following chain of events:

1. strike announced that stops all trains from going from Bay Area suburbs to San Francisco
2. a week of stand off when two BART workers were killed in an accident
3. end of strike

The hope is that topic modeling can give indication of the above three discrete events. It would be even better if it can identify pro- and anti-strike tweeets as well.

The topic model is a standard [Latent Dirichlet Allocation](http://en.wikipedia.org/wiki/Latent_Dirichlet_allocation) fitted using [gensim](http://radimrehurek.com/gensim/). 

[Full code](https://gist.github.com/tokestermw/3588e6fbbb2f03f89798) in a Gist.

### List of Words

Not really a visualization, but the easiest thing to do is to grab the top words of each topic and list them. Here is a sample:

    Top 10 terms for topic #0: expected, rep, announces, over, looks, ktvu, want, like, guys, will
    Top 10 terms for topic #1: sfgate, gridlock, normal, happy, head, real, ferries, over, runs, exactly
    Top 10 terms for topic #2: a.m., another, vote, members, other, reason, let, pass, ser…, major
    Top 10 terms for topic #3: today, killed, sanfranmag, hopes, ave, expect, delays, running, home, train

Topic 3 is most likely grouping tweets about the BART workers that were killed and to expect delays because of the incident. Topic 2 looks like union members throwing a strike are voting on .. something. Topic 1 is talking about ferries (the only other way of getting to San Francisco aside from driving) but it is not clear what these tweets are happy about. Topic 0 is looks to be random.

### Word clouds

Word clouds is a simple alternative to looking at the same data. By embiggening the most distinct words, it is easier find import words with a quick scan.

![bla](../../images/terms1.png)

Quan is a mayor of Oakland, and this topic seems to say that the deal is about to be reached. 

### PCA

It gets progressively more difficult to distinguish chaff from the signal as the number of topics increase. Reducing the topics is sometimes not an option because the topics get too general. It also becomes more difficult to automate the results so a person that haven't been looking at topic clusers for hours on end can understand.

PCA is a canonical way of reducing dimensions and it is a method that can of course be used here as well. Taking the probabities of each word for each topic, PCA can collapse the data into 2 dimensions. This makes it easily plottable. 

![bla](../../images/pca_topic.png)

Interesting how topci 19, 21 and to a some extent, 31 deviates from the other topics (I used 40 topics). Looking athe innards of each topic, all three seems to be talking about the end of the strike.

    In [231]: lda.show_topic(19)
    Out[231]:
    [(0.18418766385173357, u'tuesday'),
    (0.10941284772798156, u'over'),
    (0.074073551230934093, u'deal'),
    (0.057823820985690839, u'reached'),
    (0.040004840107066328, u'start'),
    (0.014618710538754369, u'chrisfilippi'),
    (0.01175792963040383, u'commute'),
    (0.010096535268990677, u'buses'),
    (0.0099316408990382157, u'abc7newsbayarea'),
    (0.0089298280179637094, u'late')]
    
    In [232]: lda.show_topic(21)
    Out[232]:
    [(0.19463842681026511, u'over'),
    (0.039005911200223162, u'rosenbergmerc'),
    (0.034922463036658115, u'all'),
    (0.029778810358060626, u'thank'),
    (0.018876961986207651, u'unions'),
    (0.018656417067857364, u'hopefully'),
    (0.016893084271683283, u'pissed'),
    (0.013589706807636848, u'someone'),
    (0.012154548491692339, u'per'),
    (0.011787301022370321, u'kron4news')]
    
    In [233]: lda.show_topic(31)
    Out[233]:
    [(0.073542501022656165, u'tentative'),
    (0.068444064522636891, u'reach'),
    (0.057170204108103105, u'run'),
    (0.054732038737147118, u'trains'),
    (0.054298622740944123, u'contract'),
    (0.046550628739041838, u'unions'),
    (0.041191568872948219, u'deal'),
    (0.040003874892020903, u'abc7newsbayarea'),
    (0.030594570247699304, u'agreement'),
    (0.025459332467351173, u'announcement')]

By flipping the matrix, it is trivial to repeat the analysis for words.

![bla](../../images/pca_words.png)

That is encouraging as most distinct words seem to be coming from the end of the strike. On the other hand, it is hard to tell if there are any further interesting subgroups.

### Dendrogram

So far I've used the probability weights of each word in each topic. This topic x word matrix can be transformed into a topic by topic distance (correlation) matrix to do some additional data transformations. One is clustering. Hierarchical clustering is one such technique and easily plottable as a dendrogram. 

![bla](../../images/corr.png)

The results look similar to PCA except it is easier to see the hierarchical ordering of the topics. PCA on the other hand can use any number of dimensions to see in which direction the vectors are different. 

### Force-directed graph

Using the same distance matrix, a force-directed graph can also be plotted. This basically plots the points spaced out in a certain way such that the farther the distance between two topics, the weaker the edge. I found this method to be sensitive to assumptions and it doesn't help that I don't really understand how the spacing works.

![bla](../../images/network.png)

### ...

So that's it. Four different ways to visualize topic modeling clusters. They may not be so useless after all, just that the uncertainty needs to be tamed. 
