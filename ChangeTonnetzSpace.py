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


