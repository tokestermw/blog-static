title: Frequentist - Bayesian Talking Points Memo
date: 2013-09-28
tags: frequentist, bayesian
author: Motoki Wu
summary: in all likelihood, they are similar
status: draft


So I tried to formulate some talking points to try and fit into the bootcamp format for the purposes of learning Bayesian statistics. Here it goes:

1. When we're analyzing data, we are usually interested in ... data.
2. For data, we create a **model** that we think fits to the data.
	* *e.g.* height of individuals can be modeled as a sample mean.
	* *e.g.* tomorrow's weather can be modeled using today's weather.
3. There's usually error around the model so we add a **probability distribution**, $p(X|\theta)$, 
	* $X$ is data, $\theta$ is parameter / hypothesis / belief.
4. So let's say our original model is linear: $y = \alpha + \beta x$. 
	* We can add a normal distribution to it to fit the data: $y = \alpha + \beta x + \epsilon$,
		* where $\epsilon \sim N(0, \sigma^2)$.
	* Combine the model and pdf and we get:
	 $$(\sigma\sqrt{2\pi})^{-1} e^{-\frac{1}{2\sigma^2}\left(y - (\alpha + \beta x)\right)^2}$$
	* Now we can fit by **optimizing**. 
5. For inference, we can construct **confidence intervals** and **hypothesis tests**.
6. Remember, $p(X|\theta)$ means that the data, $X$, is **random** and the parameter, $\theta$ is **fixed**. 
	* What this means is that we are assuming that data is **sampled** from a larger population.
	* Think of the parameter as the fixed, unmoving, omnipotent value for the entire population regardless of sample.
7. Since data is random, the confidence intervals that are constructed are **estimators** of the data.
	* So if $L(X)$ and $U(X)$ are lower and upper bounds of the interval, we can imagine each sample will have a **different confidence interval** around the fixed parameter.
	* Now we can say that 95% of the time, confidence intervals from infinite samples will **cover** the parameter.
8. But, but, we don't have infinite samples.
	* Of course, just like our point estimate, the confidence interval is just our current best knowledge. 
	* What doesn't change is the **estimator** for the confidence interval.
	 	* Meaning, if we keep using this estimator, it will cover the true value 95% of the time.
9. To belabor the point, we can't really inference on $\theta$ directly.
 	* *e.g.* tomorrow has a 95% chance of being between 40% ~ 60% chance of rain.
		* it's more like: I have constructed an estimator that will cover the chance of rain 95% of the time. 
10. Therefore, things like hypothesis testing came to being.
	* We don't really know $\theta$ so let's just assume $\theta = 0$.
	* Now we can at least compare the estimator with something tangible to at least be able to falsify.

Oops, this was basically **frequentist statistics**.

[WHAT IS BAYESIAN / FREQUENTIST INFERENCE?](http://normaldeviate.wordpress.com/2012/11/17/what-is-bayesianfrequentist-inference/)



A probability distribution (pdf) is basically defined as a function that integrates to one on its domain: $\int p(X|\theta)dX = 1$. 
This means that we can **sample** from the distribution.


