from sklearn import linear_model
import pickle

with open('Irrad_pickle','rb') as f:
    model = pickle.load(f)

print(model.predict([[19.62]]))
