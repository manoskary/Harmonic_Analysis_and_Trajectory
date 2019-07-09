from TrajectoryCalculationsWithClass import *


def sequencing(listOfLists, seqLen=3):
    newList = []
    listLength = len(listOfLists) - seqLen
    index = 0
    while index <= listLength:
        seqIndex = 0
        newElem = []
        while seqIndex < seqLen:
            newElem += listOfLists[index + seqIndex]
            seqIndex += 1
        newList.append(list(set(newElem)))
        index += 1
    return newList


def Trajectory3Seq(listOfChords, Tonnetz, firstPoint=(0, 0)):
    newListOfChords = sequencing(listOfChords, 3)
    return NewTrajectory(newListOfChords, Tonnetz, firstPoint)


def Trajectory3SeqRec(listOfChords, Tonnetz, firstPoint=(0, 0)):
    newListOfChords = sequencing(listOfChords, 3)
    return TrajectoryLookBefore(newListOfChords, Tonnetz, firstPoint)


def Trajectory4Seq(listOfChords, Tonnetz, firstPoint=(0, 0)):
    newListOfChords = sequencing(listOfChords, 4)
    return NewTrajectory(newListOfChords, Tonnetz, firstPoint)


def Trajectory4SeqRec(listOfChords, Tonnetz, firstPoint=(0, 0)):
    newListOfChords = sequencing(listOfChords, 4)
    return TrajectoryLookBefore(newListOfChords, Tonnetz, firstPoint)


def TrajectoryContSeq(listOfChords, Tonnetz, firstPoint=(0, 0)):
    trajectoryList = [NewTrajectory(listOfChords, Tonnetz, firstPoint)]
    n = 1
    while n <= 4:
        newListOfChords = sequencing(listOfChords, n * 4)
        trajectorylvln = NewTrajectory(newListOfChords, Tonnetz, firstPoint)
        n += 1
    return trajectoryList


def Trajectory3SeqSkip(listOfChords, Tonnetz, firstPoint=(0, 0)):
    index = 0
    newListOfChords = []
    while index <= len(listOfChords) - 3:
        newChord = listOfChords[index] + \
            listOfChords[index + 1] + listOfChords[index + 2]
        newListOfChords.append(list(set(newChord)))
        index += 3
    return TrajectoryLookBefore(newListOfChords, Tonnetz, firstPoint)
