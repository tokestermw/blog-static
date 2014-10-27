+++
title = "Statistical Shrinkage and Election Polling"
date = "2013-10-26"
tags = ["shrinkage", "politics", "r", "jags"]
+++

We saw in 2012 that this type of meta-analysis estimate can be done by anyone who is trained in advanced statistics. [Drew Linzer](http://votamatic.org/about-me/), [Sam Wang](http://election.princeton.edu/) and [Simon Jackman](http://jackman.stanford.edu/blog/) all had their models predict the election outcome very accurately. All models essentially have the same underlying state polling data and some kind of averaging methodology for the overall voter preference.

The averaging logic comes from the [James-Stein estimator](http://en.wikipedia.org/wiki/James%E2%80%93Stein_estimator). The James-Stein estimator basically says that the maximum likelihood estimate performs better on average when combined with the overall average. In other words, if the MLE shares information, or "shrunk" to the overall average, we get a more reliable estimate. The James-Stein estimator is just the weighted average of the MLE and the overall average.

$$ \hat{y} = \bar{y} + C (\hat{y}_{MLE} - \bar{y} ) $$

This logic can be extended to hierarchical models and Bayesian models where several probability distributions are combined. In the political polling context, we can greatly increase the sample size and precision without sacrificing too much bias.

## Hierarchical Forward Random Walk Model for the 2012 Presidential Election

I decided to explore shrinkage using data from the last election. I ran [Simon Jackman's hierarchical model](http://www.tandfonline.com/doi/abs/10.1080/10361140500302472#preview) on [national polling
data](http://elections.huffingtonpost.com/pollster/2012-general-election-romney-vs-obama). To simplify, I aggregated the data into weeks (instead of days) and looked at hierarchical only at the pollster level. The other folks mentioned above who were doing meta-analysis are more careful with their analysis by including informative priors, running their models on state polling data, constructing a more sophisticated time series model, etc. The statistic of interest is the proportion of Obama support relative to Romney support. The model predicting anything above 50% suggests an Obama win.

The model is simple. I fit a Binomial,

$$y_i \sim \text{Binomial}(p_i, N_i)$$

the expected value is split into a daily component and a pollster-level component,

$$\text{logit}(p\_i) = \alpha\_{t\_i} + \delta\_{j\_i}$$

the daily component is filtered with a random walk model,

$$\alpha\_t \sim N(\alpha\_{t-1}, \sigma^2\_\alpha)$$

where the spread of pollster effects are normal,

$$\delta\_j \sim N(0,\sigma^2\_\delta)$$

and it is assumed that the overall pollster effect evens out.

$$\delta\_1 = 0 - \sum^J\_{j=2} \delta\_j$$

The model is fit with [JAGS](http://mcmc-jags.sourceforge.net/). The model isn't very dynamic in the sense that it doesn't adjust for the end of the election cycle polling rush. But it does predict the right candidate. The fit of the model is shown below.

![bla](../../images/model-average.png)

The pollster effect can be quantified and is shown below.

![bla](../../images/house-bias.png)

Since the election is over, the more interesting part is the shrinkage. I calculated the James-Stein estimator for all $p_i$ and compared it against the original polling data. Even with the drift over time, we see shrinkage towards the final number.

![bla](../../images/shrinkage.png)

I decided to focus on the biggest pollsters. The biggest pollsters are the ones that get cited by media. Below I plotted on the left, all the results from YouGov and Rasmussen along with the simple average of all the polls during that week (black line). On the right hand side I put the final poll and its sampling error, compared with the hierarchical model estimate.

![bla](../../images/pooled-estimate.png)

**The JAGS code:**

	model

	## Pooling the Polls Over an Election Campaign
	## SIMON JACKMAN

	{
	  ## random walk
	  for (t in 2:T) {
	    alpha[t] ~ dnorm(alpha[t-1], tau_alpha)
	  }

	  ## not a time series, fit to polling data
	  for (i in 1:I) {
	    logit(p[i]) <- alpha[id.t[i]] + delta[id.j[i]]
	    y[i] ~ dbin(p[i], N[i])
	  }

	  ## sum to zero constraint
	  delta[1] <- 0 - sum(delta[2:J])

	  ## priors
	  alpha[1] ~ dnorm(0, .1)
	  for (j in 2:J) {
	    delta[j] ~ dnorm(0, tau_delta)
	  }

	  sigma_delta ~ dunif(0, 100)
	  tau_delta <- 1 / pow(sigma_delta, 2)

	  sigma_alpha ~ dunif(0, 100)
	  tau_alpha <- 1 / pow(sigma_alpha, 2)
	}

**Refs:**

1. Simon Jackman, Pooling the Polls Over an Election Campaign. Australian Journal of Political Science, December 2005, Vol 40, No. 4, pp. 499-517.
