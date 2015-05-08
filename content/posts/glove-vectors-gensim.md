+++
draft = false
title = "Applying GloVe Vectors using gensim word2vec"
date = 2015-05-04T07:00:00Z
tags = ["python", "word2vec", "gensim"]
+++

The word2vec algorithm is [taking the NLP world by storm](http://www.wise.io/tech/five-takeaways-on-the-state-of-natural-language-processing) as a relatively simple way of running [#deeplearning](https://twitter.com/search?q=%23deeplearning). People are looking for efficient ways of adding context to words in an effort to reduce manual labor (a.k.a. featurization). [word2vec](http://insightdatascience.com/blog/thisplusthat_a_search_engine_that_lets_you_add_words_as_vectors.html) is an unsupervised algorithm but acts like a supervised algorithm that learns on itself. It is essentially a set of logistic regressions that tries to predict a word given the surrounding words as features (or vice-versa).

[GloVe](http://nlp.stanford.edu/projects/glove/) is another algorithm that creates vector representations of words similar to word2vec. GloVe transforms the neutral network problem into a word co-occurrence matrix so it should be faster to train but uses more memory.

Like any NLP or classification task, the choice of corpus (and featurization) is paramount. Ideally, it would be great to have a large, but domain-relevant corpus. Thankfully, researchers at Stanford has provided us with large corpora of trained vectors. AFAIK the only downloadable vector corpus for Twitter is available from using GloVe.

### Vectors in gensim

The following will go through the steps to use [gensim](http://radimrehurek.com/2014/12/making-sense-of-word2vec/) to work with GloVe vectors and will use the 27 billion tokens 25 vector dimensions dataset. [1]

[1] http://www-nlp.stanford.edu/data/glove.twitter.27B.25d.txt.gz

To load the corpus into gensim, the first line of the text file has to be the number of tokens and number of vector dimensions. In this case, I use the output of `wc -l` and 25. Interestingly, the above linked corpus only contains about 1+ million (most common?) tokens. 

The next step is to simply load using gensim while being careful of tokens that are non-unicode. 

```
from os.path import join
import numpy as np
import gensim
word2vec = gensim.models.Word2Vec

GLOVE_DIR = "/dir/to/here"

def any2unicode(text, encoding='utf8', errors='strict'):
    """Convert a string (bytestring in `encoding` or unicode), to unicode."""
    if isinstance(text, unicode):
        return text
    return unicode(text.replace('\xc2\x85', '<newline>'), encoding, errors=errors)
#     return unicode(text, encoding, errors=errors)

gensim.utils.to_unicode = any2unicode
```

Once loaded, the GloVe vectors act exactly the same as word2vec vectors. The vector understands 'hurricane' is related to a natural disaster where 'storm' is more of a weather event.

```
model = word2vec.load_word2vec_format(join(GLOVE_DIR, 'glove.twitter.27B.25d.txt'), binary=False)

model.most_similar('hurricane')
[(u'storm', 0.8949791193008423),
 (u'cliff', 0.8744032979011536),
 (u'sandy', 0.8724367022514343),
 (u'wreck', 0.843888521194458),
 (u'aftermath', 0.8432317972183228),
 (u'tragedy', 0.8424368500709534),
 (u'disaster', 0.8382934927940369),
 (u'death', 0.8321377635002136),
 (u'hearing', 0.8270001411437988),
 (u'tornado', 0.8247590065002441)]

model.most_similar('storm')
[(u'hurricane', 0.8949790596961975),
 (u'fire', 0.8879387974739075),
 (u'road', 0.884390652179718),
 (u'chaos', 0.8711612224578857),
 (u'peak', 0.8681640028953552),
 (u'ground', 0.865815281867981),
 (u'madness', 0.8620372414588928),
 (u'rain', 0.8585748672485352),
 (u'collapse', 0.8583846092224121),
 (u'snow', 0.857816219329834)]
```

We can even try the canonical **_king - man + woman = queen_** exercise. Results are not as clean (unless my calculations are wrong!).

```
def get_vector(word): 
    return model.syn0norm[model.vocab[word].index]

def find_nearest(vector, K=10):
    idx = np.sum((np.square(model.syn0norm - vector)), axis=1).argsort()[:K]#.argmin()
    return map(lambda x: model.index2word[x], idx)

vector = get_vector('king') - get_vector('man') + get_vector('woman')

print find_nearest(vector)
[u'meets', u'woman', u'king', u'prince', u'queen', u'\u2019s', u'crow', u'hunter', u'father', u'soldier']
```

There are many ways to improve performance: add vectors, add tokens, filter by language and filter out spam, having a more concentrated filter, add ngrams, etc. Or it may well be that Twitter doesn't have a good semantic understanding of kings and queens.

[gist:](https://gist.github.com/tokestermw/cb87a97113da12acb388) to preprocess the tweets in the same way as the GloVe authors in Python.
