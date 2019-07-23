from Data_and_Dicts import dictOfTonnetz


def TonnetzToString(Tonnetz):
    if Tonnetz == [3, 4, 5]:
        TonnetzString = 'T345'
    elif Tonnetz == [1, 3, 8]:
        TonnetzString = 'T138'
    elif Tonnetz == [1, 4, 7]:
        TonnetzString = 'T147'
    elif Tonnetz == [1, 2, 9]:
        TonnetzString = 'T129'
    elif Tonnetz == [2, 3, 7]:
        TonnetzString = 'T237'
    else:
        raise ValueError()
    return TonnetzString


# TODO just Take a Chord and Place the first Note.
def PlaceFirstNote(listOfChords, Tonnetz):
    try:
        firstNote = listOfChords[0][0]
        return dictOfTonnetz[TonnetzToString(Tonnetz)][firstNote]
    except:
        print("This Tonnetz's Initial position is not defined")
        return (0, 0)
