import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn import preprocessing


# Don't forget that points should be in the form of an array, that is :
# [[x1, y1, z1], [x2, y2, z2], ...]

def kNN(label, points):
    X = np.array(points)
    y = np.dot(X, [1.0, 1.0, 1.0])
    lab_enc = preprocessing.LabelEncoder()
    y_enc = lab_enc.fit_transform(y)
    knn = KNeighborsClassifier()
    knn.fit(X, y_enc)
    return knn

# Requested format dict['composer'] = listOfPoints (all analyzed pieces of
# the composer)


def classification(dictOfComposerPoints):
    knnDict = dict()
    for composer, listOfPoints in dictOfComposerPoints.items():
        knnDict[composer] = kNN(composer, listOfPoints)
    return knnDict
