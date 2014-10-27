+++
title = "Comparing Crowdsourced and Government Fukushima Radiation Data"
date = "2013-11-21"
tags = ["python", "javascript", "flask"]
+++

## Mapping the Difference between Crowdsourced and Government Data

I decided it might be a good exercise to actually check between the two datasets. My main objective is to create an app that plots both data, interpolate the data for direct comparison and quantify the difference. Since the data are high resolution both in time and space, I thought it was best to let the user get a feel of what the difference were.

The government data is 23+ static points around Fukushima Daiichi with radiation measured every 10 minutes. The crowdsourced data is measured using sensors attached to volunteers' cars. Therefore, I did an interpolation on the government data but not the crowdsourced data for the comparison.

### Interpolation Methods

I used three different interpolation methods. I did this to reduce model error and to not get accused of cherry-picking models to fail to reject my null (H0: Government = Crowdsourced).

*Inverse Distance Weighting*: This is the simplest model. Farther off points are less related to the interpolated point than closer ones. I could have also used k-nearest neighbors but that was overkill for a basic model to compare against.

*Radial Basis Network*: RBNs are a type of neural network that takes radial activation functions (Gaussian in my case, I've also looked at splines) at each data point and and fits linear weights to get the interpolated point. Since I'm interpolating, the centers of the radial functions are known so back propagation is not needed. Linear weights are fit using the matrix inverse ([ref](http://math.bu.edu/people/mkon/nnpap3.pdf)).

*Ordinary Kriging*: I can estimate the linear weights by minimizing the MSE. This breaks up into variance, covariance and semivariance so I fit the variogram, then run the interpolation. Since kriging assumes a normal random field, a confidence interval can be calculated. Looking ahead, ordinary kriging assumes the same mean for all points so universal kriging may be more apropos.

I fit and train them offline to make it ready for the interactive app.

### Comparison

The comparison between the two datasets is simple. I do a log on both datasets, and then for each point from the crowdsourced data, I run the interpolation on the government data for that location. I take a ratio of these points and plot them on a map.

To compare between the interpolation methods, I considered leave one out cross-validation MSEs, K-fold cross-validation with respect to latitude and ditto with longitude. I also considered interpolated points that are closer to the crowdsourced points as "better." Generally, the kriging method performed the best.

### Map App

The app ([here](http://54.200.81.28:5000/)[link broken]) allows users to play with the data and its comparisons. The user can choose the date, choose the model, choose the CPM-to-µSv/hr conversion rate and choose the "percentage difference." The conversion rate [defaults to 300](http://blog.safecast.org/2011/06/volunteer-report-safecasting-miyagi-by-rob-kneller/) so 300 CPM is equivalent to 1µSv/hr. The "percentage difference" just lets you choose how far apart the two values need to be to consider it significant. So choosing 10% means that if the citizen data is within +/-10% of the government data, the marker on the map is set to <font color="green">green</font>.

Here is a sample output from 09-24-2011 (kriging, 300, 10%):

![bla](../..//images/ok.png)

The <font color="red">red markers</font> are when the government data is bigger than the crowdsourced data, the <font color="blue">blue markers</font> are when the crowdsourced data is bigger and the <font color="green">green markers</font> shows anything between +/-10% of each other.

So the results look pretty good. You can check for other dates but the kriging method approximates the crowdsourced data pretty well. The data diverge most around the epicenter of where the meltdown was. This isn't too surprising since it's where the radiation is the highest and most variable. For this date, the median ratio between crowdsourced and government data was ~98%.

### Unit Conversion

A very important detail is the unit conversion rate. I defaulted to 300, but since it's measuring different things (electron count vs. radiation exposure), there is no perfect conversion. The conversion may be different depending on sensor, location, wind etc. So below is a plot of median crowdsourced to government ratio for different conversion rates:

![bla](../../images/conversion_profile.png)

At least for 09-24-2013, the optimal conversion rate is 270. Whether that is the best conversion it's not possible to know given this data.

### No clear difference

For this set of data, I found no telling difference. Interpolation does not work well outside the interpolated points by definition and the results become more unstable as you get closer to the epicenter. All in all, it's good to have multiple datasets as checks on the system

## Links

* [Link to Government Data](http://www.sendung.de/japan-radiation-open-data/), [Link to Crowdsourced Data](http://blog.safecast.org/).
* [GitHub Repo](https://github.com/tokestermw/fukushima-nuclear-radiation)
* [App](http://54.200.81.28:5000/)
