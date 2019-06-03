import music21 as ms
from itertools import product
import ast

def parseMidi(midifile):
    mfile = ms.converter.parse(midifile)
    mChords = mfile.chordify()
    chordList = []
    chordVectors = []
    for c in mChords.recurse().getElementsByClass('Chord'):
        chordList.append(c.orderedPitchClasses)
        chordVectors.append(c.intervalVector)
    print('The number of chords found is : ',  len(chordList))
    return chordList, chordVectors
    

def Connected(l1, x, y, z):
    j = 0
    for i in l1:
        if (
           sum(i) - 2*(i[x] + i[y] + i[z]) < 0 
        ):
            j += 1
    return j

def TonnetzConnectivity(chordVectors):
    TonnetzConnectivity = {
        'T129' : Connected(chordVectors, 0, 1 ,2),
        'T138' : Connected(chordVectors, 0, 2 ,3),
        'T147' : Connected(chordVectors, 0, 3 ,4),
        'T156' : Connected(chordVectors, 0, 4 ,5),
        'T237' : Connected(chordVectors, 1, 2 ,4),
        # 'T246' : Connected(chordVectors, 1, 3 ,5),
        'T345' : Connected(chordVectors, 2, 3 ,4)
    }
    GetTheBestTonnetz = max(TonnetzConnectivity, key=TonnetzConnectivity.get)  # Just use 'min' instead of 'max' for minimum.
    print('The Tonnetz Selected is :', GetTheBestTonnetz, '\n' + 'The number of represented chords in this system is :', TonnetzConnectivity[GetTheBestTonnetz])
    return(GetTheBestTonnetz)

def TonnetzConfig(GetTheBestTonnetz):
    if GetTheBestTonnetz == 'T129' :
        Tonnetz = [1, 2, 9]
    elif GetTheBestTonnetz == 'T138' :
        Tonnetz = [1, 3, 8]
    elif GetTheBestTonnetz == 'T147' :
        Tonnetz = [1, 4, 7]
    elif GetTheBestTonnetz == 'T156' :
        Tonnetz = [2, 5, 6]
    elif GetTheBestTonnetz == 'T237' :
        Tonnetz = [2, 3, 7]
    # elif GetTheBestTonnetz == 'T246' :
    #     Tonnetz = [2, 4, 6]
    elif GetTheBestTonnetz == 'T345' :
        Tonnetz = [3, 4, 5]
    return Tonnetz


def findIfConnected(interval, T_axes):
    axe1 = T_axes[0]
    axe2 = T_axes[1]
    axe3 = T_axes[2]
    if interval == axe1:
        value = 1
    elif interval == axe2:
        value = 1
    elif interval == axe3 :
        value = 1
    elif interval == (12 - axe3):
        value = 1
    elif interval == (12 - axe2):
        value = 1
    elif interval == (12 - axe1):
        value = 1
    else :
        value = 0
    return value

def removeDoubles(l, lvec):
    N = len(l)
    nlpc = []
    nlVec = []
    sl = [str(i) for i in l]
    nlpc.append(l[0])
    nlVec.append(lvec[0])
    for i in range(1,N):
        if sl[i] != sl[i-1]:
            nlpc.append(ast.literal_eval(sl[i]))
            nlVec.append(lvec[i])
    return nlpc, nlVec

def checkEdges(chord, T_axes):
    if len(chord) == 1 :
        return False
    else:
        constrain = True
        pdct = product(chord, chord)
        edges = []
        # from a chord take the cartesian product and keep those couples that form an interval on the axes
        for (a,b) in pdct:
            if findIfConnected((a-b)%12, T_axes) == 1 :
                edges.append((a, b))
        if edges != [] :
            l, l2 = zip(*edges)
        else :
            l = []
        # If a note is not contained in the edges return false
        for el in chord:
            if el not in l:
                constrain = False
        # If all the above is satisfied check if an edge is isolated
        if constrain == True :
            for (a, b) in edges:
                if l.count(a) == 1 and l.count(b) == 1:
                    constrain = False
        return constrain
    
def checkConnectivity(listofchords, currentindex, chord, T_axes, alpha):
    if alpha < 3 :
        conexCondition = checkEdges(chord, T_axes)
        if conexCondition == False:
            my_set = set(listofchords[currentindex]+listofchords[currentindex-alpha])
            NewChord = list(my_set)
            alpha += 1
            # Recursive call
            return checkConnectivity(listofchords, currentindex, NewChord, T_axes, alpha)
        else :
            return chord
    else :
        print(chord)
        raise RuntimeError('Infinite Loop')
       
    
def removeNonConnected(l1, l2, T_axes):
    axe1 = T_axes[0] - 1
    axe2 = T_axes[1] - 1
    if T_axes[2] > 6:
        axe3 = (12 - T_axes[2]) - 1
    else : 
        axe3 = T_axes[2] - 1
    nl1 = l1
    nl2 = []
    nl3 = []
    for i, vector in enumerate(l2):
        k = sum(vector) - 2*(vector[axe1] + vector[axe2] + vector[axe3])
        if (
           k < 0 
        ):
            nl2.append(vector)
        else :
            chord = l1[i]
            kappa = checkConnectivity(l1, i, chord, T_axes, 1)
            del nl1[i]
            nl1.insert(i, kappa)
    return nl1, nl2




def fromMidiToPCS(midifile):
    chordList, chordVectors = parseMidi(midifile)
    Tonnetz = TonnetzConfig(TonnetzConnectivity(chordVectors))
    chordListNoDoubles, chordListNoDoublesVec = removeDoubles(chordList, chordVectors)
    print('After duplicate reduction the number of chords is :', len(chordListNoDoubles))
    chordListConnect, vectorsListConnect = removeNonConnected(chordListNoDoubles, chordListNoDoublesVec, Tonnetz)
    print(len(chordListConnect))
    return chordListConnect, Tonnetz