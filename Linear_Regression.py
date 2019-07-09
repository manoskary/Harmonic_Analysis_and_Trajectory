import numpy as np
from sklearn.linear_model import LinearRegression
from structural_functions import get_closest_value, getKeyByValue
from Data_and_Dicts import labels

from NetworkX_GraphTranslation import CentralityPoint2D as cepo
from AutoHarmonicAnalysis import GraphOfNewPiece
# Don't forget that points should be in the form of an array, that is :
# [[x1, y1, z1], [x2, y2, z2], ...]

# label = a*x[0] + b*x[1] + c*x[2] + d


def regression(label, points):
    X = np.array(points)
    y = X
    reg = LinearRegression().fit(X, y)
    return reg

# Requested format dict['composer'] = listOfPoints (all analyzed pieces of
# the composer)


def classification(dictOfComposerPoints):
    regressionDict = dict()
    for composer, listOfPoints in dictOfComposerPoints.items():
        regressionDict[composer] = regression(composer, listOfPoints)
    return regressionDict


def dictOfPredict(point, regDict):
    preDict = dict()
    for composer, reg in regDict.items():
        preDict[composer] = reg.predict(np.array([point]))
    return preDict


def predict_lin_reg(regDict):
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


def predict_midi(compDict):
    regDict = classification(compDict)
    prediction = predict_lin_reg(regDict)
    return prediction
