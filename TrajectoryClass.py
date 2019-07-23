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

# ADD MIDI FILE PROPERTIES

    def addNumberOfInstruments(self, numberOfInstruments):
        self.numOfInstr = numberOfInstruments

    def addInstruments(self, listOfInstruments):
        self.instruments = list(set(listOfInstruments))
        self.addNumberOfInstruments(len(set(listOfInstruments)))

# Find a way to estimate tempo
    def addTempo(self, tempo):
        self.tempo = tempo

    def addNumber_of_signature_changes(self, number):
        self.number_of_signature_changes = number

    def addTime_signature_changes(self, signature_changes):
        self.time_signature_changes = list(set(signature_changes))
        self.addNumber_of_signature_changes(len(signature_changes))
