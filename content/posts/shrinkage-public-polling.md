title: Statistical Shrinkage and Election Polling
date: 2013-10-26
tags: shrinkage, politics, r, jags
author: Motoki Wu
summary: anything you can do I can do something similar

<style>
img[alt=bla] {width: 400px;}
</style>

The 2012 U.S. Presidential Election is long past over but not before Nate Silver basically [revolutionized](http://deadspin.com/espns-nate-silver-is-here-to-answer-your-questions-951328525) political reporting. Political reporting defaults to laying blame on both major parties equally to the 18th significant figure. This is analogous to setting an uninformative (maximum entropy) prior to your model each time you do a story. I think this quote sums up the skepticism of reporters and talk show hosts have towards data-based reporting:

> Nate Silver says this is a 73.6 percent chance that the president is going to win? ... anybody that thinks that this race is anything but a tossup right now is such an ideologue, they should be kept away from typewriters, computers, laptops and microphones for the next 10 days, because they’re jokes.<cite>[Joe Scarborough](http://www.politico.com/blogs/media/2012/10/nate-silver-romney-clearly-could-still-win-147618.html)</cite>

Nate Silver includes his model results as an an integral component of political reporting. If every outlet does something similar to their election coverage (and they are starting to), it would have the effect of anchoring voter preferences (no more poll chasing) and providing a non-partisan, evidenced view of the current state of the race (no more "race is tight so watch our show!"). 

We saw in 2012 that this type of meta-analysis estimate can be done by anyone who is trained in somewhat advanced statistics. [Drew Linzer](http://votamatic.org/about-me/), [Sam Wang](http://election.princeton.edu/) and [Simon Jackman](http://jackman.stanford.edu/blog/) all had their models predict the election outcome very accurately. All models essentially have the same underlying state polling data and some kind of averaging methodology for the overall voter preference. 

The averaging logic comes from the [James-Stein estimator](http://en.wikipedia.org/wiki/James%E2%80%93Stein_estimator). The James-Stein estimator basically says that the maximum likelihood estimate performs better on average when combined with the overall average. In other words, if the MLE shares information, or "shrunk" to the overall average, we get a more reliable estimate. The James-Stein estimator is just the weighted average of the MLE and the overall average.

$$ \hat{y} = \bar{y} + C (\hat{y}_{MLE} - \bar{y} ) $$

This logic can be extended to hierarchical models and Bayesian models where several probability distributions are combined. In the political polling context, we can greatly increase the sample size and precision without sacrificing too much bias (assuming that there are not any substantial systematic biases). 

## Hierarchical Forward Random Walk Model for the 2012 Presidential Election

I decided to explore shrinkage using data from the last election. I ran [Simon Jackman's hierarchical model](http://www.tandfonline.com/doi/abs/10.1080/10361140500302472#preview) on [national polling
data](http://elections.huffingtonpost.com/pollster/2012-general-election-romney-vs-obama). To simplify, I aggregated the data into weeks (instead of days) and looked at hierarchical only at the pollster level. The other folks mentioned above who were doing meta-analysis are more careful with their analysis by including informative priors, running their models on state polling data, constructing a more sophisticated time series model, etc. The statistic of interest is the proportion of Obama support relative to Romney support. The model predicting anything above 50% suggests an Obama win.

The model is simple. I fit a Binomial,

$$y_i \sim \text{Binomial}(p_i, N_i)$$

the expected value is split into a daily component and a pollster-level component,

$$\text{logit}(p_i) = \alpha_{t_i} + \delta_{j_i}$$

the daily component is filtered with a random walk model,

$$\alpha_t \sim N(\alpha_{t-1}, \sigma^2_\alpha)$$

where the spread of pollster effects are normal,

$$\delta_j \sim N(0,\sigma^2_\delta)$$

and it is assumed that the overall pollster effect evens out. 

$$\delta_1 = 0 - \sum^J_{j=2} \delta_j$$

The model is fit with [JAGS](http://mcmc-jags.sourceforge.net/). The model isn't very dynamic in the sense that it doesn't adjust for the end of the election cycle polling rush. But it does predict the right candidate. The fit of the model is shown below. 

![bla](|filename|/images/model-average.png)

The pollster effect can be quantified and is shown below. 

![bla](|filename|/images/house-bias.png)

Since the election is over, the more interesting part is the shrinkage. I calculated the James-Stein estimator for all $p_i$ and compared it against the original polling data. Even with the drift over time, we see shrinkage towards the final number. 

![bla](|filename|/images/shrinkage.png)

I decided to focus on the biggest pollsters. The biggest pollsters are the ones that get cited by media. Below I plotted on the left, all the results from YouGov and Rasmussen along with the simple average of all the polls during that week (black line). On the right hand side I put the final poll and its sampling error, compared with the hierarchical model estimate. 

![bla](|filename|/images/pooled-estimate.png)

You can see how tenuous it is to rely on one pollster, much less one poll to narrate voter support. Even the simple average is fairly noisy and "riggable" by prolific pollsters. CNN is funnily even-handed. You see that the hierarchical Bayesian model performs well and much more even-handed (in the scientific sense). 

I would also like to note that it is actually fairly easy to construct an accurate model at least for the national election. The data is simple to use and copious. Pollsters generally do a good job of sampling voter preferences except for a few notables (Gallup). Any kind of averaging algorithm can get pretty close so competition to construct the best model will only get more fierce. I suspect Nate Silver is changing employers because of this very reason ;)

**The JAGS code:**

	:::jags
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