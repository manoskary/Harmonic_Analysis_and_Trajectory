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

def coordRot(value, rotation) : 
	x, y = value
	if rotation == 90 :
		newvalue = (-y, x)
	elif rotation == 180 :
		newvalue = (-x, -y)
	else :
		newvalue = (y, -x)
	return newvalue

def noteRot(key, value, rotation, Tonnetz) :
	x, y = coordRot(value, rotation)
	newkey = getKeysByValue(Tonnetz, (abs(x%3), abs(y%4)))
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




