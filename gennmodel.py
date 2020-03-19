from sklearn import linear_model
import pickle

with open('Genn_pickle','rb') as f:
    model = pickle.load(f)

print(model.predict([[6213.217]]))
