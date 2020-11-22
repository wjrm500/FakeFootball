import Utils
import os
import matplotlib.pyplot as plt
from math import ceil, sqrt
import numpy as np
from sklearn.linear_model import LinearRegression
from scipy.stats import pearsonr
import pickle
from scipy.optimize import curve_fit

file = open('list79133', 'rb')
data = pickle.load(file)
file.close()

# for feature in list(data[0]['features'].keys()):
#     print(feature)

# for key, value in list(data[0]['features'].items()):
#     print(key, value)

x = [[value for value in item['features'].values()] for item in data]
y = [item['labels']['rank'] for item in data]

x, y = np.array(x), np.array(y)
model = LinearRegression().fit(x, y)

Utils.pickleObject(model)


# curve_fit(lambda t, a, b: a + b * np.log(t),  x,  y)











# model = Utils.unpickleMostRecent(os.getcwd())

# for coefficient in model.coef_:
#     print(coefficient)

# x_new = [[75, 0.90, 0.1]]
# x_new = np.array(x_new)

# y_pred = model.predict(x_new)
# print('predicted response:', y_pred, sep='\n')





# x = [item['features']['strength'] for item in data]
# y = [item['labels']['rank'] for item in data]

# features = list(data[0]['features'].keys())
# features.remove('formation')
# i = 0
# for feature in features:
#     if feature == 'bestPlayer' + str(i):
#         x = [item['features'][feature] for item in data]
#         # print('Player rank: {} - Correlation: {}'.format(feature, pearsonr(x, y)[0]))
#         print(pearsonr(x, y)[0])
#         i += 1

# numFeatures = len(features)
# numRows = ceil(sqrt(numFeatures))
# numCols = numRows - 1 if numRows * numRows - 1 > numFeatures else numRows

# fig, axes = plt.subplots(numRows, numCols)
# for ax, feature in zip(axes.flatten(), features):
#     x = [item['features'][feature] for item in data]
#     ax.title.set_text(feature)
#     ax.hist2d(x, y, (10, 20), cmap=plt.cm.jet)
# plt.show()

# x = [item['features']['strength'] for item in data]
# y = [item['features']['depth'] for item in data]

# plt.scatter(x, y, s = 1)
# plt.show()