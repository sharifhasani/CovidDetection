# -*- coding: utf-8 -*-
"""DenseNet169-learning_rate(0.3,...,0.9).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12X7_U5EF_-lB_REHBlh8pK3NpcbpLFBG

# import libraries
"""

from glob import glob
import cv2
from matplotlib import pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split

from keras.applications import VGG16, ResNet50, MobileNet, MobileNetV2, InceptionV3, Xception, DenseNet169
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing import image
from keras.layers import Dense, Flatten
from tensorflow.keras.models import Model, Sequential
from keras.losses import SparseCategoricalCrossentropy, CategoricalCrossentropy
from keras.optimizers import SGD
from xgboost import XGBClassifier

from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC

"""# Get Dataset

download
"""

! wget https://github.com/muhammedtalo/COVID-19/archive/refs/heads/master.zip

"""extract files"""

! unzip -q master.zip -d /content

"""# Load Data

load images directory
"""

images_path = {}
images_path["Covid"] = glob("/content/COVID-19-master/X-Ray Image DataSet/Covid-19/*.png")
images_path["Covid"] += glob("/content/COVID-19-master/X-Ray Image DataSet/Covid-19/*.jpeg")
images_path["Covid"] += glob("/content/COVID-19-master/X-Ray Image DataSet/Covid-19/*.jpg")

images_path["NoFindings"] = glob("/content/COVID-19-master/X-Ray Image DataSet/No_findings/*.png")
images_path["NoFindings"] += glob("/content/COVID-19-master/X-Ray Image DataSet/No_findings/*.jpeg")
images_path["NoFindings"] += glob("/content/COVID-19-master/X-Ray Image DataSet/No_findings/*.jpg")

images_path["Pneumonia"] = glob("/content/COVID-19-master/X-Ray Image DataSet/Pneumonia/*.png")
images_path["Pneumonia"] += glob("/content/COVID-19-master/X-Ray Image DataSet/Pneumonia/*.jpeg")
images_path["Pneumonia"] += glob("/content/COVID-19-master/X-Ray Image DataSet/Pneumonia/*.jpg")

print(images_path["Covid"])
print(images_path["NoFindings"])
print(images_path["Pneumonia"])

images_class = {
    "Covid": 0,
    "Pneumonia": 1,
    "NoFindings": 2
}

X = []
Y = []

for label in images_path:
    for image_path in images_path[label]:
        image = cv2.imread(image_path)
        image = cv2.resize(image,(224, 224))
        X.append(image)
        Y.append(images_class[label])

plt.imshow(X[0])
plt.show()

print(np.array(X).shape)
print(np.array(Y).shape)
print(Y[0])

"""# Build model

build model and get features
"""

x = np.array(X)
y = np.array(Y)


# initial pre trained model
pre_trained_models = {}
pre_trained_models["DenseNet169"] = DenseNet169(include_top=False, input_shape=(224, 224, 3))

print(np.array(x).shape)

"""# Split train and test data

slpit and make flatten features
"""

X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size=0.2)


X_train = pre_trained_models["DenseNet169"].predict(X_train)
X_test = pre_trained_models["DenseNet169"].predict(X_test)

flatten_feature_train = []
for item in X_train:
    flatten_feature_train.append(item.flatten())

flatten_feature_train = np.array(flatten_feature_train)

flatten_feature_test = []
for item in X_test:
    flatten_feature_test.append(item.flatten())

flatten_feature_test = np.array(flatten_feature_test)

"""# Classification

initial XGBoost classifier
"""

Y_pred = {}
result = {}

# learning_reate = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
# print(learning_reate)
for lr in [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
    print(f"\n=======learning_reate {lr}=====")
    XGB_Classifier = XGBClassifier(n_estimator=100, learning_rate=lr)
    print(f"features shape : ", flatten_feature_train.shape)

    XGB_Classifier.fit(flatten_feature_train, Y_train)


    Y_pred[lr] = XGB_Classifier.predict(flatten_feature_test)

    result[lr] = {}
    result[lr]["Accuracy score"] = accuracy_score(Y_test, Y_pred[lr])
    result[lr]["confusion matrix"] = confusion_matrix(Y_test, Y_pred[lr])
    result[lr]["f1 score"] = f1_score(Y_test, Y_pred[lr], average="macro")
    result[lr]["precision score"] = precision_score(Y_test, Y_pred[lr], average="macro")
    result[lr]["recall score"] = recall_score(Y_test, Y_pred[lr], average="macro")

    print(f"\nAccuracy score : ", result[lr]["Accuracy score"])
    print(f"\nconfusion matrix : \n", result[lr]["confusion matrix"])
    print(f"\nf1 score : ", result[lr]["f1 score"])
    print(f"\nprecision score : ", result[lr]["precision score"])
    print(f"\nrecall score : ", result[lr]["recall score"])

"""fit XGBoost classifier"""

print(result)

XGB_Classifier.fit(flatten_feature_train, Y_train)

Y_pred = XGB_Classifier.predict(flatten_feature_test)

"""print result"""

result["Accuracy score"] = accuracy_score(Y_test, Y_pred)
result["confusion matrix"] = confusion_matrix(Y_test, Y_pred)
result["f1 score"] = f1_score(Y_test, Y_pred, average="macro")
result["precision score"] = precision_score(Y_test, Y_pred, average="macro")
result["recall score"] = recall_score(Y_test, Y_pred, average="macro")


print(f"\n============")
print(f"\nAccuracy score : ", result["Accuracy score"])
print(f"\nconfusion matrix : \n", result["confusion matrix"])
print(f"\nf1 score : ", result["f1 score"])
print(f"\nprecision score : ", result["precision score"])
print(f"\nrecall score : ", result["recall score"])