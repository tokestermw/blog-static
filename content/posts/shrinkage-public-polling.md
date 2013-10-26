title: bla
date: 2013-10-26
tags: shrinkage, politics, r, ggplot2, jags
author: Motoki Wu
summary: something witty
status: draft

## i need to put an image

![shrinkage](|filename|/images/shrinkage.png)
![model average](|filename|/images/model-average.png)
![house bias](|filename|/images/house-bias.png)


the winbugs model

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

