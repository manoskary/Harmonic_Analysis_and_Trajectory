from Data_and_Dicts import dictOfTonnetz, dictOfTonnetze
from structural_functions import getKeyByValue


def TonnetzToString(Tonnetz):
    TonnetzString = getKeyByValue(dictOfTonnetze, Tonnetz)
    return TonnetzString


# TODO just Take a Chord and Place the first Note.
def PlaceFirstNote(listOfChords, Tonnetz):
    try:
        firstNote = listOfChords[0][0]
        return dictOfTonnetz[TonnetzToString(Tonnetz)][firstNote]
    except:
        print("This Tonnetz's Initial position is not defined")
        return (0, 0)
