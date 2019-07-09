from Data_and_Dicts import *


def TonnetzToString(Tonnetz):
    if Tonnetz == [3, 4, 5]:
        Tonnetz = 'T345'
    elif Tonnetz == [1, 3, 8]:
        Tonnetz = 'T138'
    elif Tonnetz == [1, 4, 7]:
        Tonnetz = 'T147'
    elif Tonnetz == [1, 2, 9]:
        Tonnetz = 'T129'
    elif Tonnetz == [2, 3, 7]:
        Tonnetz = 'T237'
    else:
        raise ValueError()
    return Tonnetz


def PlaceFirstNote(listOfChords, Tonnetz):
    if Tonnetz == [3, 4, 5]:
        firstnote = listOfChords[0][0]
        position = NotePointsT345[firstnote]
    elif Tonnetz == [1, 3, 8]:
        firstnote = listOfChords[0][0]
        position = NotePointsT138[firstnote]
    elif Tonnetz == [1, 4, 7]:
        firstnote = listOfChords[0][0]
        position = NotePointsT147[firstnote]
    elif Tonnetz == [1, 2, 9]:
        firstnote = listOfChords[0][0]
        position = NotePointsT129[firstnote]
    elif Tonnetz == [2, 3, 7]:
        firstnote = listOfChords[0][0]
        position = NotePointsT237[firstnote]
    else:
        position = (0, 0)
    return position
