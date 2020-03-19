import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#also known as scikit learn
from sklearn import linear_model
#split data
from sklearn.model_selection import train_test_split
from sklearn.metrics import explained_variance_score, mean_squared_error, r2_score
from sklearn.metrics import confusion_matrix
data = pd.read_csv('irrad_gen - Sheet1.csv')
print(data.head())
print("dimension")
print("Rad:{}".format(data.Irrad.ndim))
print("Gen:{}".format(data.generation.ndim))
print("Shape")
print("Rad:{}".format(data.Irrad.shape))
print("Gen:{}".format(data.generation.shape))
X = data.iloc[:, 0].values.reshape(-1, 1)
Y = data.iloc[:, 1].values.reshape(-1, 1)
print("dimension")
print("Rad:{}".format(X.ndim))
print("Gen:{}".format(Y.ndim))
print("Shape")
print("Rad:{}".format(X.shape))
print("Gen:{}".format(Y.shape))
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.33, random_state=42)
reg = linear_model.LinearRegression()
reg.fit(X_train,y_train)
print(reg.predict([[6213.217]]))

import pickle
with open("Genn_pickle","wb") as f:
    pickle.dump(reg,f)
