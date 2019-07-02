from AutoHarmonicAnalysis import BachTrajectoryGraphs, GetWorksByComposer, GetWorksByDirectory, getPiecesOutOfDistribution, twoDictsDistCompare, SortPiecesByDistances
from PlottingGraphCentrality import CentralitiesScatterPlot, Centralities2DPlot
import os

directory = input("Enter the directory of your files : ")
isDirectory = os.path.isdir(directory)
while not isDirectory :
	directory = input("The directory wasn't valid enter another directory : ")
	isDirectory = os.path.isdir(directory)

composer = input("Enter A Composer's Name : ")

Bach = BachTrajectoryGraphs(200)
Directory = GetWorksByDirectory(directory)
Composer = GetWorksByComposer(composer)

CentralitiesScatterPlot(Bach, Directory, Composer)
CentralitiesScatterPlot(Bach, Directory, Composer, 'Mix2')
CentralitiesScatterPlot(Bach, Directory, Composer, 'Mix3')
CentralitiesScatterPlot(Bach, Directory, Composer, 'Mix4')
CentralitiesScatterPlot(Bach, Directory, Composer, 'Eigenvalues')
CentralitiesScatterPlot(Bach, Directory, Composer, 'Closeness')

print("The max is : ", getPiecesOutOfDistribution(Bach))
print("The max is : ", getPiecesOutOfDistribution(Directory))
print("The max is : ", getPiecesOutOfDistribution(Composer))

print("Comparison between Bach and " + directory + " : ", twoDictsDistCompare(Bach, Directory))
print("Comparison between Bach and ", composer + " : ", twoDictsDistCompare(Bach, Composer))
print("Comparison between " + composer + "and " + directory + " : " , composertwoDictsDistCompare(Composer, Directory))

print(" SortPiecesByDistances : ")
print(SortPiecesByDistances(Bach))
print(SortPiecesByDistances(Composer))
print(SortPiecesByDistances(Directory))
