title: Frequentist - Bayesian Talking Points Memo
date: 2013-09-28
tags: frequentist, bayesian
author: Motoki Wu
summary: in all likelihood, they are similar
status: draft

I [previously mentioned](http://tokestermw.github.io/posts/zipfian-academy-week-2-log-naive-bayesian-learning.html) that it's hard to learn theory fast. So I tried to formulate some talking points to learn Bayesian statistics that fits into the bootcamp format. Here it goes:

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
	* Now we can at least compare the estimator with something tangible so we're able to falsify.

Oops, this was basically **frequentist statistics**. Try again:

1. When we're analyzing data, we are usually interested in ... parameters.
2. Start with $p(\theta)$, the **prior** distribution.
3. We can update the prior by the **data** distribution $p(X | \theta)$.
4. Arriving at the **posterior** distribution $p(\theta | X)$.
	* How do we calculate this?
5. From above, take $p(X|\theta)$ and flip the conditionals using Bayes' Theorem:
$$ p(\theta|X) = \frac{p(X|\theta)p(\theta)}{\int p(X|\theta)p(\theta) d\theta} $$
6. So we can estimate by optimizing like before right?
	* We *can*, but it's usually too complicated.
	* We also want to express our posterior as a probability distribution.
	* We cannot just ignore the integral in the denominator.
7. A probability distribution basically is just something that sums to one: $\int p(X)dX = 1$.
	* We like this so we can **simulate** from the distribution.
	* Also like because results are in probabilities.
8. Just simulating isn't an answer since again, the functional form is too complex.
	* We know how to simulate from a Normal distribution, but Bayesian models usually are shaped like [NaN](http://ile-maurice.tripod.com/naan.htm).
9. So we simulate, but we use a smart simulation that traverses the distribution without getting stuck in local optima.
	* The dumb approach would be to randomly pick numbers on a grid and calculate the function value.
	* Smarter algorithms use a distribution that we know how to sample from as a basis to simulate from the posterior.
10. **Estimation** and **integration** of the posterior is done by Markov chain Monte Carlo (MCMC) -- the smart approach.
11. **Markov Chain**:
	* A chain of samples from a distribution that is only dependent on the immediate past.
	* The dependency enables us to traverse the probability distribution smartly.
	* Only dependent on the past state so we can snip and cut out samples as necessary.
	* Under certain conditions, markov chains should converge to the posterior.
	* The samples from the posterior should be independent, just like any other distribution.
12. **Monte Carlo**:
	* Monte Carlo integration allows us to calculate integrals using simulations.
		* So for $M$ simulations from $p(\theta_i)$:
		$$\int p(X|\theta)p(\theta) d\theta \approx \frac{1}{M}\sum_i p(X|\theta_i)$$
	* We use the **law of large numbers** to get a bunch of random samples from the posterior that will converge.
	* Once we have the samples from the converged posterior, we can use **Monte Carlo integration** to calculate test statistics of our liking.
13. Finally, inference on $\theta$.
	* If you want to test if the posterior is greater than 0, just do:
	 	* ```(sum(theta) > 0) / len(theta)```. 

Frequentist methods are easier to set up the model and do the estimation than Bayesian methods. Whereas Bayesian methods are easier to do inference and model checking. 

Sometimes the goals are different. Frequentist methods may be more interested in describing the general properties of the population. Bayesian methods may be more interested in the immediate (ever-changing) dataset. 

I managed to not mention likelihood methods until now, but really at its core, both methods are solving the same function.


