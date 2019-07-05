from FirstNotePosition import *


def getKeysByValue(dictOfElements, valueToFind):
    listOfKeys = list()
    for key, value in dictOfElements.items():
        if value == valueToFind :
            return key

def noteChange(key, value, newTonnetz) :
	x, y = value
	newkey = getKeysByValue(newTonnetz, (x%4, y%3))
	return newkey


def chordDictToNewTonnetz(chordDict, newTonnetz) :	
	newchordDict = dict()
	for key, value in chordDict.items() :
		newkey = noteChange(key, value, newTonnetz)
		newchordDict[newkey] = value
	return newchordDict

def trajectoryToNewTonnetz(trajectory, newTonnetz) :
	newlistOfChords = []
	newTonnetz = dictOfTonnetz[newTonnetz]
	for chordDict in trajectory.chordPositions :
		newchordDict = chordDictToNewTonnetz(chordDict, newTonnetz)
		newlistOfChords.append(list(newchordDict.keys()))
	return(newlistOfChords)


# TODO fixed coordinates to equilateral triangles to rotate but didn't fix back coordinates.
def coordRot(value, rotation) : 
	x, y = value
	# x = x + 0.5*y
	# y = 0.87*y
	if rotation == 90 :
		newvalue = ( -y , x)
	elif rotation == 180 :
		newvalue = (-x, -y)
	elif rotation == 270:
		newvalue = (y, -x)
	else : 
		newvalue =  (x, y)
	return newvalue

def noteRot(key, value, rotation, Tonnetz) :
	x, y = coordRot(value, rotation)
	newkey = getKeysByValue(Tonnetz, (x%3, y%4))
	return newkey


def chordDictRot(chordDict, rotation, Tonnetz) :	
	newchordDict = dict()
	for key, value in chordDict.items() :
		newkey = noteRot(key, value, rotation, Tonnetz)
		newchordDict[newkey] = value
	return newchordDict



def trajectoryRot(trajectory, rotation=180) :
	newlistOfChords = []
	Tonnetz = TonnetzToString(trajectory.Tonnetz)
	Tonnetz = dictOfTonnetz[Tonnetz]
	for chordDict in trajectory.chordPositions :
		newchordDict = chordDictRot(chordDict, rotation, Tonnetz)
		newlistOfChords.append(list(newchordDict.keys()))
	return(newlistOfChords)




