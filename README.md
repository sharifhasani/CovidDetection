# CovidDetection
Here we're going to classify given CXR images and distinguish whether if there is any sign of covid-19, pneumonia or not. In this documentation  only the methods that gave us the best results are included in the code.

## Dataset
click here to [download](https://github.com/sharifhasani/CovidDetection/tree/master/dataset/X-Ray%20Image%20DataSet) dataset

## How it works?
in this code we're using extracted features of each image and then use classification methods for classify images

## Feature Extraction
we used DenseNet169 pre trained convolutional neural network for extract featurs 
Throughout implementing this project, we have found best parameters for each classification(binary and multi classification). So the model is trained with 1664 features per each image.

## Classification
### Classifiers:
* XGBoost classifier

So far the best and fastest classifier is XGBoost classifier and it gave us the highest accuracy of all.

## Accuracy
98.2 is the highest percentage of accuracy we have reached so far, we reached this accuracy by using XGBoost classifier.

## Performance Metrics
Because our class distribution is imbalanced, we determined metrics beside accuracy, such as precision, sensitivity, specificity and f1-score.
