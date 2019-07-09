
class TrajectoryGraph:

    def __init__(self, trajectory):
        firstPoint = PlaceFirstNote(chordList, Tonnetz)
        Points, listOfBeetweenEdges = NewTrajectory(
            chordList, Tonnetz, firstPoint)
        Edges = TrajectoryNoteEdges(Points) + listOfBeetweenEdges
        setOfPoints, multiSetOfPoints = SetOfPoints(Points)
        TrajectoryPoints[newPiece] = np.array(setOfPoints)
        TrajectoryPointWeights[newPiece] = weightsOfTrajPoints(
            setOfPoints, multiSetOfPoints)
        TrajectoryEdges[newPiece] = Edges
        self.graph = CreateGraph(Points, Edges)
