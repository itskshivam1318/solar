import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#also known as scikit learn
from sklearn import linear_model
#split data
from sklearn.model_selection import train_test_split
from sklearn.metrics import explained_variance_score, mean_squared_error, r2_score
from sklearn.metrics import confusion_matrix
data = pd.read_csv('temp_irrad - Sheet1.csv')
print(data.head())
print("dimension")
print("Temp:{}".format(data.temp.ndim))
print("Irrad:{}".format(data.Irrad.ndim))
print("Shape")
print("Temp:{}".format(data.temp.shape))
print("Irrad:{}".format(data.Irrad.shape))
X = data.iloc[:, 0].values.reshape(-1, 1)
Y = data.iloc[:, 1].values.reshape(-1, 1)
print("dimension")
print("Temp:{}".format(X.ndim))
print("Irrad:{}".format(Y.ndim))
print("Shape")
print("Temp:{}".format(X.shape))
print("Irrad:{}".format(Y.shape))
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.33, random_state=42)
reg = linear_model.LinearRegression()
reg.fit(X_train,y_train)
print(reg.predict([[35.223]]))

import pickle
with open("Irrad_pickle","wb") as f:
    pickle.dump(reg,f)
