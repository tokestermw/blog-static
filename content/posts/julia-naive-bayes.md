+++
draft = false
title = "Naive Bayes Classifier on Epicurious Recipes using Julia"
date = 2014-07-12T07:00:36Z
tags = ["julia", "food", "naive bayes"]
+++

This is adapted from an [IJulia](https://github.com/JuliaLang/IJulia.jl) Notebook. It runs a
naive Bayes classifier on some [Epicurious](http://www.epicurious.com) recipe
data as an exercise to learn more [Julia](http://julialang.org).

A better, more Julia-like implementation of Naive Bayes is
[here](https://github.com/johnmyleswhite/NaiveBayes.jl).

### Convenience functions

Each line of the data contains the name of the cuisine, then the list of
ingredients. I create a `RaggedMatrix` type (alias) to deal with string data of
indeterminate length. The `parse` function will split the data into ingredients
and cuisines. I also have a `count_vector` that counts the items in a single
dimension array (or a vector in R sense, or a list in Python sense).


    typealias RaggedMatrix{T} Array{Array{T,1},1}

    function parse(filename)
        file = readlines(open(filename))

        x = convert(RaggedMatrix{String},
                [apply(vcat, [rstrip(term) for term in split(line, '\t')[2:end]])
                 for line in file])
        y = convert(Array{String,1},
                [split(line, '\t')[1] for line in file])

        return(x, y)
    end

    function count_vector(v::Array)
        v_counts = Dict()
        v_uniq = unique(v)
        for name in v_uniq
            counts = sum([i == name for i in v])
            push!(v_counts, name, counts)
        end
        v_counts
    end

### Data

[Data](http://yongyeol.com/data/scirep-cuisines-detail.zip) is from Yong-Yeol Ahn from a paper that was fairly well noticed (food
networks, not that kind). There are other recipes but I decided to use
Epicurious.

    filename = "../data/scirep-cuisines-detail/epic_recipes.txt"

    x, y = parse(filename)

    # number of recipes
    length(y)

    13408

    # count all the cuisines
    y_counts = count_vector(y)
    [i for i in y_counts]

    26-element Array{Any,1}:
     ("Mexican",622)
     ("Chinese",226)
     ("Moroccan",137)
     ("Cajun_Creole",146)
     ("Mediterranean",289)
     ("Central_SouthAmerican",241)  
     ("Southwestern",108)
     ("English_Scottish",204)
     ("Thai",164)
     ("Japanese",136)
     ("Scandinavian",92)
     ("African",115)
     ("Greek",225)
     ("German",52)
     ("Indian",274)
     ("MiddleEastern",248)
     ("American",4988)
     ("Asian",1176)
     ("French",996)
     ("Irish",86)
     ("Italian",1715)
     ("Jewish",320)
     ("Spanish_Portuguese",291)
     ("Vietnamese",65)
     ("EasternEuropean_Russian",146)
     ("Southern_SoulFood",346)

    # each document is a recipe
    y[1], x[1]

    ("Vietnamese",String["vinegar","cilantro","mint","olive_oil","cayenne","fish","lime_juice","shrimp","lettuce","carrot","garlic","basil","cucumber","rice","seed","shiitake"])

    # create lookup dictionaries
    all_cuisines = unique(y)
    cuisines = (String=>Int64)[all_cuisines[i] => i for i in 1:length(all_cuisines)]
    rev_cuisines = (Int64=>String)[cuisines[i] => i for i in all_cuisines]

    all_ingredients = unique(apply(vcat, [line for line in x]))
    ingredients = (String=>Int64)[all_ingredients[i] => i for i in 1:length(all_ingredients)]
    rev_ingredients = (Int64=>String)[ingredients[i] => i for i in all_ingredients]

### Vectorize -> Fit -> Predict

Vaguely following the sci-kit model, I write functions for vectorization, fitting
and prediction.

    # ingredients x cuisines (feature x class) matrix
    # count the words for each cuisine
    function count_vectorizer(x::RaggedMatrix{String}, y::Array{String,1},
        features::Dict{String,Int64}, classes::Dict{String,Int64})


        X = zeros(length(features), length(classes))

        # Julia is column dominant
        for c in keys(classes)
            features_for_class = apply(vcat, [i for i in x[find(_ -> _ == c, y)]])
            for f in features_for_class
                @inbounds X[features[f], classes[c]] += 1.0
            end
        end
        X
    end

    @timed X = count_vectorizer(x, y, ingredients, cuisines)

    (
    350x26 Array{Float64,2}:
     15.0   31.0   79.0  18.0  127.0   41.0  …   11.0  56.0  20.0  397.0  17.0
     24.0   79.0   30.0  18.0    7.0   75.0      43.0   5.0   4.0  244.0  56.0
     21.0   35.0    7.0  14.0   19.0    7.0      20.0   2.0   4.0   97.0   2.0
      2.0   40.0  183.0  80.0  307.0   75.0     100.0  47.0  27.0   78.0  43.0
     30.0  125.0   70.0  21.0   38.0  125.0      40.0  84.0   3.0  345.0  88.0
     51.0   11.0   24.0  14.0   68.0    8.0  …   10.0   2.0   6.0  228.0   0.0
     30.0   26.0   15.0   3.0    8.0   41.0       3.0   4.0   3.0  195.0  29.0
     12.0   18.0   31.0   0.0   12.0   13.0       1.0  14.0   1.0  142.0   2.0
      9.0    5.0    3.0   3.0   21.0    8.0       0.0   3.0   6.0   58.0   6.0
     18.0   21.0   12.0  40.0  108.0    7.0      21.0  11.0   8.0  145.0   6.0
     47.0  114.0  167.0  60.0  272.0  137.0  …   63.0  89.0  19.0  565.0  67.0
     18.0    3.0    6.0   4.0   69.0    1.0       6.0   8.0   5.0   66.0   0.0
     11.0   20.0   15.0   8.0   23.0    3.0       4.0   2.0   8.0   92.0   2.0
      ⋮                                 ⋮    ⋱                             ⋮  
      0.0    0.0    0.0   0.0    0.0    0.0       0.0   0.0   0.0    0.0   0.0
      0.0    0.0    0.0   0.0    0.0    0.0       0.0   0.0   0.0    0.0   0.0
      0.0    0.0    0.0   0.0    0.0    0.0  …    0.0   0.0   0.0    0.0   0.0
      0.0    0.0    0.0   0.0    0.0    0.0       0.0   0.0   0.0    0.0   0.0
      0.0    0.0    0.0   0.0    0.0    0.0       0.0   0.0   0.0    0.0   0.0
      0.0    0.0    0.0   0.0    0.0    0.0       0.0   0.0   0.0    0.0   0.0
      0.0    0.0    0.0   0.0    0.0    0.0       0.0   0.0   0.0    0.0   0.0
      0.0    0.0    0.0   0.0    0.0    0.0  …    0.0   0.0   0.0    0.0   0.0
      0.0    0.0    0.0   0.0    0.0    0.0       0.0   0.0   0.0    0.0   0.0
      0.0    0.0    0.0   0.0    0.0    0.0       0.0   1.0   0.0    0.0   0.0
      0.0    0.0    0.0   0.0    0.0    0.0       0.0   0.0   1.0    0.0   0.0
      0.0    0.0    0.0   0.0    0.0    0.0       0.0   0.0   0.0    1.0   0.0,

    0.44882671,10309732)

    print(sum(X, 1))
    print(size(X))

    [737.0 2804.0 2664.0 2510.0 8279.0 2184.0 1715.0 1957.0 759.0 1997.0 43541.0 1220.0 2330.0 1311.0 14436.0 685.0 5695.0 2177.0 504.0 2498.0 1160.0 1482.0 3055.0 1658.0 11644.0 1123.0](350,26)

    function naive_bayes_fit(X::Array{Float64,2}, alpha::Float64 = 1.0)

        log_like = zeros(size(X))

        # sum over classes
        total = sum(X, 1)

        # sum over rows for each class for performance reasons
        for j in 1:size(X)[2]
            @inbounds log_like[:,j] = log(X[:,j] .+ alpha) .- log(total[j])
        end

        log_like
    end

    @timed log_like = naive_bayes_fit(X)

    (
    350x26 Array{Float64,2}:
     -3.83     -4.47307  -3.50556  -4.8836   …  -4.36884  -3.37609  -4.13339
     -3.38371  -3.55678  -4.4536   -4.8836      -5.80393  -3.86129  -2.98071
     -3.51155  -4.35528  -5.80814  -5.11999     -5.80393  -4.77758  -5.92515
     -5.50398  -4.22523  -2.67265  -3.43359     -4.08116  -4.9931   -3.23957
     -3.1686   -3.10252  -3.6249   -4.737       -6.02707  -3.51611  -2.53512
     -2.65134  -5.4539   -4.66871  -5.11999  …  -5.46746  -3.92882  -7.02376
     -3.1686   -4.64297  -5.115    -6.44174     -6.02707  -4.08443  -3.62256
     -4.03764  -4.99436  -4.42185  -7.82804     -6.72022  -4.3997   -5.92515
     -4.3      -6.14704  -6.50129  -6.44174     -5.46746  -5.28501  -5.07785
     -3.65815  -4.84776  -5.32263  -4.11447     -5.21614  -4.37894  -5.07785
     -2.73139  -3.19387  -2.76362  -3.71716  …  -4.41764  -3.02395  -2.80425
     -3.65815  -6.55251  -5.94167  -6.2186      -5.62161  -5.15785  -7.02376
     -4.11768  -4.89428  -5.115    -5.63081     -5.21614  -4.82995  -5.92515
      ⋮                                      ⋱                       ⋮
     -6.60259  -7.9388   -7.88758  -7.82804     -7.41337  -9.36255  -7.02376
     -6.60259  -7.9388   -7.88758  -7.82804     -7.41337  -9.36255  -7.02376
     -6.60259  -7.9388   -7.88758  -7.82804  …  -7.41337  -9.36255  -7.02376
     -6.60259  -7.9388   -7.88758  -7.82804     -7.41337  -9.36255  -7.02376
     -6.60259  -7.9388   -7.88758  -7.82804     -7.41337  -9.36255  -7.02376
     -6.60259  -7.9388   -7.88758  -7.82804     -7.41337  -9.36255  -7.02376
     -6.60259  -7.9388   -7.88758  -7.82804     -7.41337  -9.36255  -7.02376
     -6.60259  -7.9388   -7.88758  -7.82804  …  -7.41337  -9.36255  -7.02376
     -6.60259  -7.9388   -7.88758  -7.82804     -7.41337  -9.36255  -7.02376
     -6.60259  -7.9388   -7.88758  -7.82804     -7.41337  -9.36255  -7.02376
     -6.60259  -7.9388   -7.88758  -7.82804     -6.72022  -9.36255  -7.02376
     -6.60259  -7.9388   -7.88758  -7.82804     -7.41337  -8.6694   -7.02376,

    0.020244006,644824)

    function naive_bayes_predict(predict::Array{String,1}, log_like::Array{Float64,2},
        prior::Array{Float64,1}, features::Dict{String,Int64}, rev_classes::Dict{Int64,String})

        results = zeros(length(rev_classes))

        for i in 1:length(rev_classes)
            ind = convert(Array{Int64,1}, [features[i] for i in predict]) # not sure why i have to do this
            results[i] = sum(log_like[ind, i]) + log(prior[i])
        end

        rev_classes[indmax(results)]
    end

    prior = ones(length(cuisines)) / length(cuisines)

### Prediction

Now I can predict the cuisine given a list of ingredients.


    # A prediction
    i = 3
    y[i], naive_bayes_predict(x[i], log_like, prior, ingredients, rev_cuisines), x[i]

    ("Vietnamese","Vietnamese",String["garlic","soy_sauce","lime_juice","thai_pepper"])

    # another one
    i = 3000
    y[i], naive_bayes_predict(x[i], log_like, prior, ingredients, rev_cuisines), x[i]

    ("American","German",String["cane_molasses","butter","wheat","vanilla","ginger","honey","nutmeg","cinnamon","lard","egg","milk"])

I can create a confusion matrix to see the overlap of the ingredients between
cuisines.

    confusion_matrix = zeros(length(cuisines), length(cuisines))

    for i in keys(cuisines)
        cuisine = x[find(_ -> _ == i, y)]
        total = length(cuisine)
        for j in cuisine
            predicted = naive_bayes_predict(j, log_like, prior, ingredients, rev_cuisines)
            confusion_matrix[cuisines[i], cuisines[predicted]] += 1 / total
        end
    end

    confusion_matrix

    26x26 Array{Float64,2}:
     0.907692    0.0         0.0         …  0.0         0.0         0.0
     0.0218978   0.627737    0.0            0.0328467   0.00364964  0.0255474
     0.0274914   0.00343643  0.42268        0.0824742   0.0         0.0652921
     0.00625     0.009375    0.0125         0.065625    0.0         0.021875  
     0.0100402   0.00401606  0.0291165      0.195783    0.00100402  0.0060241
     0.0207469   0.0165975   0.0746888   …  0.0829876   0.00414938  0.190871  
     0.0205479   0.00684932  0.0            0.0616438   0.00684932  0.0273973
     0.365854    0.0304878   0.0            0.0         0.0304878   0.00609756
     0.0         0.0108696   0.0            0.0869565   0.0         0.0
     0.0         0.00444444  0.00444444     0.0311111   0.0         0.00444444
     0.0280674   0.0114274   0.0252606   …  0.152165    0.00240577  0.0643545
     0.026087    0.0521739   0.0173913      0.0347826   0.0         0.00869565
     0.00806452  0.0322581   0.0201613      0.0322581   0.0         0.016129  
     0.00684932  0.00684932  0.0205479      0.143836    0.0         0.0273973
     0.00116618  0.00116618  0.0268222      0.0874636   0.0         0.0110787
     0.0         0.0         0.0         …  0.0930233   0.0         0.0
     0.0369775   0.00803859  0.0144695      0.0498392   0.0         0.302251  
     0.039823    0.00884956  0.0            0.00884956  0.0265487   0.00442478
     0.0         0.0         0.0            0.115385    0.0         0.0192308
     0.0         0.0103806   0.0484429      0.0484429   0.0         0.0138408
     0.0441176   0.00735294  0.0         …  0.0220588   0.0147059   0.0
     0.00729927  0.0364964   0.0145985      0.0145985   0.0         0.00729927
     0.00867052  0.00289017  0.0144509      0.106936    0.0         0.0606936
     0.00980392  0.00980392  0.0196078      0.485294    0.0         0.00490196
     0.182823    0.0280612   0.0            0.0102041   0.0637755   0.00935374
     0.00925926  0.00925926  0.0185185   …  0.00925926  0.0185185   0.685185  

What is the cuisine that is easiest to predict? Vietnamese.

    confuse = diag(confusion_matrix)
    sort([(rev_cuisines[i], confuse[i]) for i in 1:length(cuisines)])

    26-element Array{(Any,Any),1}:
     ("African",0.32173913043478275)
     ("American",0.00541299117882919)
     ("Asian",0.06377551020408168)
     ("Cajun_Creole",0.7054794520547963)
     ("Central_SouthAmerican",0.2531120331950211)
     ("Chinese",0.756637168141594)
     ("EasternEuropean_Russian",0.26027397260273977)
     ("English_Scottish",0.48529411764705815)
     ("French",0.14156626506024103)
     ("German",0.7692307692307696)
     ("Greek",0.6088888888888881)
     ("Indian",0.6277372262773735)
     ("Irish",0.6627906976744192)
     ("Italian",0.4740524781341024)
     ("Japanese",0.7794117647058805)
     ("Jewish",0.3406249999999993)
     ("Mediterranean",0.33217993079584757)
     ("Mexican",0.29099678456591677)
     ("MiddleEastern",0.3225806451612901)
     ("Moroccan",0.6131386861313863)
     ("Scandinavian",0.6304347826086959)
     ("Southern_SoulFood",0.3930635838150301)
     ("Southwestern",0.6851851851851855)
     ("Spanish_Portuguese",0.422680412371133)
     ("Thai",0.4878048780487808)
     ("Vietnamese",0.9076923076923062)

Looks like "Asian" cuisine is so general that the classifier cannot predict
correctly. Let's see what it's confused with.

    confuse = confusion_matrix[cuisines["Asian"],:]
    [(rev_cuisines[i], confuse[i]) for i in 1:length(cuisines)]

    26-element Array{(Any,Any),1}:
     ("Vietnamese",0.18282312925170086)
     ("Indian",0.028061224489795925)
     ("Spanish_Portuguese",0.0)
     ("Jewish",0.004251700680272108)
     ("French",0.002551020408163265)
     ("Central_SouthAmerican",0.0008503401360544217)  
     ("Cajun_Creole",0.005952380952380952)
     ("Thai",0.10034013605442185)
     ("Scandinavian",0.006802721088435374)
     ("Greek",0.002551020408163265)
     ("American",0.0008503401360544217)
     ("African",0.006802721088435374)
     ("MiddleEastern",0.0017006802721088435)
     ("EasternEuropean_Russian",0.0008503401360544217)
     ("Italian",0.002551020408163265)
     ("Irish",0.003401360544217687)
     ("Mexican",0.002551020408163265)
     ("Chinese",0.31037414965986226)
     ("German",0.028911564625850348)
     ("Mediterranean",0.0)
     ("Japanese",0.2176870748299322)
     ("Moroccan",0.00510204081632653)
     ("Southern_SoulFood",0.0017006802721088435)
     ("English_Scottish",0.010204081632653059)
     ("Asian",0.06377551020408168)
     ("Southwestern",0.009353741496598638)

Yup, "Asian" is confused with other Asian cuisines.
