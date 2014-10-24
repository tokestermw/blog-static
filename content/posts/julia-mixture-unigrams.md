+++
title = "Mixture of Unigrams in Julia"
date = "2014-06-14"
tags = ["food", "julia", "topic modeling"]
draft = true
+++

### Naive Bayes Gibbs Sampler

For one document $area$

$$ p(\theta | X) \propto \prod_{i=1...N} p(X_i|\theta)p(\theta)$$

A full Bayesian Naive Bayes, call it Naive Bayesian.

Replace $$p(\theta)$$ with a binomial distribution for the class:

$$p(z|\theta) \sim Bernoulli(\theta)$$

where the prior is

$$p(\theta | \alpha) \sim Beta(\alpha)$$

The likelihood is the same (this should be an index that is extracted!)

$$ p(X_i | \phi_z) \sim Multinomial(\phi_z) $$

and the prior for the word distribution

$$p(\phi | \beta) \sim Dirichlet(\beta)$$

The full joint distribution for one document is

$$p(z, \theta, X | \alpha, \beta) $$

For $d = 1...D$ documents and and $i = 1...N_d$ words for each document, the full joint distribution is as follows:

$$ p(\theta | \alpha) p(\phi | \beta) \prod\_{d=1..D} p(z\_d|\theta) \prod\_{d=1..D}\prod\_{i=1..N\_d}p(X\_{id}|\phi\_{z\_d})$$

Now let's write each components mathematically.

There's actually two hyperparameters (two classes) for the beta prior to the Bernoulli.

$$p(\theta|\alpha_1, \alpha_2) \propto \theta^{\alpha_1-1} (1-\theta)^{\alpha_2-1}$$

Now let's look at the Dirichlet prior on the words. The hyperparameter is actually a vector.

$$ p(\phi|\beta) \propto \prod_{i=1..N_d} \phi_i^{\beta_i-1} $$

where $\phi\_{N\_d} = 1 - \sum\_{i=1}^{N\_d-1}\phi\_i$.

Now the topic distribution or the Bernoulli for yes and no.

$$p(z_d|\theta) \propto \theta^{z_d} (1-\theta)^{1-z_d} $$

And then the categorical distribution:

$$p(X\_{id}|\phi\_{z\_d}) = \prod\_{i=1..N\_d} \phi\_{z\_d}^{[X\_{id}=i]}$$

The categorical distribution is a close cousin to the multinomial distribution where it's basically a multinomial distribution of size 1, except the output is not a vector, but an index. This index is useful when picking topics and picking words given a topic.

The Dirichlet prior is conjugate to the categorical distribution.

Let $c_1, ..., c_V$ be the counts of the words in a document. Then the Categorical-Dirichlet distribution is just a Dirichlet distribution with parameters:
