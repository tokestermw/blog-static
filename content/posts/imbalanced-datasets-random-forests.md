+++
title = "SMOTE Algorithm to Classify Imbalanced Datasets with Random Forests"
date = "2014-07-29"
tags = ["random forests", "python", "SMOTE"]
+++

Imbalanced datasets occur often in real-life classification problems. In credit card fraud detection, fraud may occur less than .01% of all transactions. The usual maximum likelihood or risk minimization methods put equal weight to each data point; thus, the estimation problem is overwhelmed by the majority class. 

Rare occurrences of an event are usually the most interesting part of the problem. We'd like a way to compensate for this asymmetry. 

### Adding weights / cost function

The easiest thing to do is just add weights to each class so their approximately equal. Say there are 99 samples of class 0 and 1 sample of class 1, then we multiply (1/99) to class 0.

In scikit-learn there usually an option to equalize the classes:

    from sklearn.svm import SVC

    clf = SVC()
    clf_fit = clf.fit(x, y, class_weight = 'auto')

For random forests:

    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import balance_weights

    clf = RandomForestClassifier()
    clf_fit = clf.fit(x, y, sample_weight = balance_weights(y))

There can also be a cost function to get the optimal weight proportions and treat the weights as hyperparameters.

Unfortunately, a highly imbalanced dataset with highly asymmetric weights will have a very "spiky" optimization surface. Weights may work if the rare class has enough variance in the data. But most likely the classification results will be inconsistent.

### Resampling

Another approach is bootstrap resampling. Resampling ameliorates the "spiky" problem somewhat by oversampling the rare class to match the sample size of the majority class[es]. The resampling can be combined with undersampling of the majority class[es].

If the rare class is not sufficiently varied enough, the optimization surface can get "blocky."

### SMOTE (Synthetic Minority Oversampling Technique)

To increase the variability of the rare class, you can take advantage of the majority class. The [SMOTE](https://www.jair.org/media/953/live-953-2037-jair.pdf) was developed for this purpose. Resampling takes into account the correlations of the features between data points.

The SMOTE algo. is as follows:

* For each data point for the rare class
    * Grab K nearest neighbors from the entire dataset
    * For however many times you would like to resample
        * Randomly pick a neighbor
        * Calculate the distance between the neighbor and the original data point
        * Randomly choose a point between the two points and use that as a resample

So if being poor and irresponsiveness are features that generally predict credit card fraud, you would want to resample the data with similar features. There is some randomization / shrinkage to smooth out resamples. 

### Test

So I ran a test using a random forests classifier on made up data. I generated imbalanced binary data where the ratio is 99:1. I calculated the ROC curve of the results for 1) just using weights to adjust the imbalanced, and 2) using the SMOTE algorithm.

Full code in a [Gist](https://gist.github.com/tokestermw/487971ee8b297f5749d1).

![bla](../../images/ROC_two.png)

The red line shows the ROC curve for the SMOTE algorithm and the blue line for the weights method. I plotted the thresholds of classification as well. In general, the SMOTE method pushed the ROC curve to the upper left (better, but not by much). The bigger change comes from the thresholds. If we assume a canonical threshold of 0.5, the improvement to recall is about 0.22. We don't want to rely on a tiny threshold since they are inconsistent. 

There are of course trade-offs to this method. The more similar you make the resamples to the original dataset, the harder it is to predict new rare cases outside of he dataset.

### The code for the SMOTE algorithm.

    """
    SMOTE: Synthetic Minority Over-sampling Technique
    Chawla, Bowyer, Hall, Kegelmeyer
    Journal of Artificial Intelligence Research 16 (2002) 321-357
     
    https://www.jair.org/media/953/live-953-2037-jair.pdf
    """
     
    import warnings
    import random
     
    import numpy as np
    from sklearn.neighbors import NearestNeighbors
     
    def smote(T, N, K):
        """
        T ~ an array-like object representing the minority matrix
        N ~ the percent oversampling you want. e.g. 500 will give you 5 samples
        from the SMOTE algorithm (thus, has to be multiple of 100).
        K ~ K Nearest Neighbors
        """
     
        ## make sure T is an array with the proper dimensions
        T = np.asarray(T, dtype = np.float)
        nsamples = T.shape[0]
        nfeatures = T.shape[1]
        if nsamples < nfeatures:
            warnings.warn("Make sure the features are in the columns.")
        
        ## we want to oversample
        if N < 100:
            raise Exception("N should be at least 100")
     
        N = int(N) / 100
     
        nn = NearestNeighbors(K)
        
        nn.fit(T)
     
        synthetic = np.zeros([N * nsamples, nfeatures])
        
        for sample in xrange(nsamples):
            nn_minority = nn.kneighbors(T[sample], return_distance = False)[0]
            N_next = N
            
            newindex = 0
            while N_next != 0:
                k_chosen = random.randint(0, K - 1)
                while nn_minority[k_chosen] == sample: # don't pick itself
                    k_chosen = random.randint(0, K - 1)                
                
                for feature in xrange(nfeatures):
                    diff = T[nn_minority[k_chosen], feature] - T[sample, feature]
                    gap = random.uniform(0, 1)
                    synthetic[N*sample + newindex, feature] = T[sample, feature] + gap * diff
                
                newindex += 1
                N_next -= 1
     
        return synthetic


