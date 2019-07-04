import numpy as np
from sklearn.linear_model import LinearRegression

labels = {
	'bach' : [0, 0, 0],
	'palestrina' : [1, 0, 0],
	'beethoven' : [0, 0, 1],
	'mozart' : [0, 1, 0],
	'monteverdi' : [0, 1, 1],
	'schuann' : [1, 1, 0],
	'chopin' : [1, 0, 1],
	'standardJazz' : [1, 1, 1]
}

def listOfPoints2array(points) :
	newList = []
	for point in points :
		x, y, z = point
		newList.append([x, y, z])
	return newList

# label = a*x[0] + b*x[1] + c*x[2] + d
def regression(points, label) :
	y = labels[label]
	X = np.array(listOfPoints2array(points))
	reg = LinearRegression().fit(X, y)
	return reg.score(X, y), reg.coef_, reg.intercept_


#Requested format dict['composer'] = listOfPoints (all analyzed pieces of the composer)

def classification(dictOfComposerPoints) :
	regressionDict = dict()
	for composer, listOfPoints in dictOfComposerPoints.items() :
		regressionDict[composer] = regression(listOfPoints, composer)
	return regressionDict