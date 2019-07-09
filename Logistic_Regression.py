import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn import preprocessing
from structural_functions import get_closest_value, getKeyByValue
from Data_and_Dicts import labels

from NetworkX_GraphTranslation import CentralityPoint2D as cepo
from AutoHarmonicAnalysis import GraphOfNewPiece

# Don't forget that points should be in the form of an array, that is :
# [[x1, y1, z1], [x2, y2, z2], ...]

# label = a*x[0] + b*x[1] + c*x[2] + d


def log_reg(label, points):
    X = np.array(points)
    y = np.dot(X, labels[label])
    lab_enc = preprocessing.LabelEncoder()
    y_enc = lab_enc.fit_transform(y)
    reg = LogisticRegression()
    reg.fit(X, y_enc)
    return reg

# Requested format dict['composer'] = listOfPoints (all analyzed pieces of
# the composer)


def classification(dictOfComposerPoints):
    regDict = dict()
    for composer, listOfPoints in dictOfComposerPoints.items():
        regDict[composer] = log_reg(composer, listOfPoints)
    return regDict


def dictOfPredict(point, regDict):
    preDict = dict()
    for composer, reg in regDict.items():
        print(composer, reg.decision_function(np.array([point])))
        preDict[composer] = reg.predict_proba(np.array([point]))
    return preDict


def predict_log_reg(regDict):
    fileName = input("Enter the name of your File : ")
    directory = input("Enter the Directory of your File : ")
    completeName = fileName + '.mid'

    graph = GraphOfNewPiece(completeName, directory)
    x, y, z = cepo(graph[completeName], 3, 'Mix')
    point = [x, y, z]

    preDict = dictOfPredict(point, regDict)
    label = getKeyByValue(
        preDict,
        get_closest_value(
            list(
                preDict.values()),
            1.))
    return label, preDict
