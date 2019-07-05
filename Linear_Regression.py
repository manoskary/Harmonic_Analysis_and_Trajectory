import numpy as np
from sklearn.linear_model import LinearRegression

labels = {
	'bach' : [0, 0, 0],
	'palestrina' : [1, 0, 0],
	'beethonven' : [0, 0, 1],
	'mozart' : [0, 1, 0],
	'monteverdi' : [0, 1, 1],
	'schumann' : [1, 1, 0],
	'chopin' : [1, 0, 1],
	'jazz' : [1, 1, 1]
}


# Don't forget that points should be in the form of an array, that is : [[x1, y1, z1], [x2, y2, z2], ...]

# label = a*x[0] + b*x[1] + c*x[2] + d
def regression(label, points) :
	X = np.array(points)
	y = np.dot(X, labels[label])
	reg = LinearRegression().fit(X, y)
	return reg

#Requested format dict['composer'] = listOfPoints (all analyzed pieces of the composer)

def classification(dictOfComposerPoints) :
	regressionDict = dict()
	for composer, listOfPoints in dictOfComposerPoints.items() :
		regressionDict[composer] = regression(composer, listOfPoints)
	return regressionDict

def get_closest_value(arr, target):
    n = len(arr)
    left = 0
    right = n - 1
    mid = 0

    # edge case - last or above all
    if target >= arr[n - 1]:
        return arr[n - 1]
    # edge case - first or below all
    if target <= arr[0]:
        return arr[0]
    # BSearch solution: Time & Space: Log(N)

    while left < right:
        mid = (left + right) // 2  # find the mid
        if target < arr[mid]:
            right = mid
        elif target > arr[mid]:
            left = mid + 1
        else:
            return arr[mid]

    if target < arr[mid]:
        return find_closest(arr[mid - 1], arr[mid], target)
    else:
        return find_closest(arr[mid], arr[mid + 1], target)

def find_closest(val1, val2, target):
    return val2 if target - val1 >= val2 - target else val1

