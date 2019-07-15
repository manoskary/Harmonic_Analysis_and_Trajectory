class TrajectoryClass:

    def __init__(self, initialChordPosition, listOfChords, Tonnetz):
        self.chordPositions = [initialChordPosition]
        self.connectingEdges = []
        self.index = 1
        self.listOfChords = listOfChords
        self.Tonnetz = Tonnetz

    def addChord(self, chordPosition, connectingEdge):
        self.chordPositions.append(chordPosition)
        self.connectingEdges.append(connectingEdge)
        self.index += 1

    def getLastPosition(self, offset=1):
        if offset > self.index:
            raise IndexError()
        return self.chordPositions[-offset]

    def getThisChord(self):
        return self.listOfChords[self.index]

    def getNextChord(self, offset=1):
        return self.listOfChords[self.index + offset]

    def addType(self, trajType):
        self.type = trajType

    def addNumberOfInstruments(self, numberOfInstruments):
        self.numOfInstr = numberOfInstruments

    def addInstruments(self, listOfInstruments):
        self.instruments = listOfInstruments
        self.addNumberOfInstruments(len(listOfInstruments))


