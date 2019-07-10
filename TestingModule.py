from AutoHarmonicAnalysis import BachTrajectoryGraphs, GetWorksByComposer, GetWorksByDirectory
from AutoHarmonicAnalysis import getPiecesOutOfDistribution, twoDictsDistCompare, SortPiecesByDistances
from PlottingGraphCentrality import CentralitiesScatterPlot
import os
from music21 import corpus

directory = input("Enter the directory of your files : ")
isDirectory = os.path.isdir(directory)
while not isDirectory:
    directory = input("The directory wasn't valid enter another directory : ")
    isDirectory = os.path.isdir(directory)
directorystyle = input("What is the style of the directory?")

composer = input("Enter A Composer's Name : ")
isValidList = corpus.getComposer(composer)
while isValidList == []:
    composer = input(
        "The Composer's name wasn't valid enter another composer : ")
    isValidList = corpus.getComposer(composer)

imageDirectory = input("Enter the directory to save the plots : ")
isDirectory = os.path.isdir(imageDirectory)
while not isDirectory:
    imageDirectory = input(
        "The directory wasn't valid enter another directory : ")
    isDirectory = os.path.isdir(imageDirectory)


Composer = GetWorksByComposer(composer)
Directory = GetWorksByDirectory(directory)
Bach = BachTrajectoryGraphs(200)

CentralitiesScatterPlot(
    Bach,
    Directory,
    Composer,
    'Mix',
    imageDirectory,
    "Bach",
    directorystyle,
    composer)
CentralitiesScatterPlot(
    Bach,
    Directory,
    Composer,
    'Mix2',
    imageDirectory,
    "Bach",
    directorystyle,
    composer)
CentralitiesScatterPlot(
    Bach,
    Directory,
    Composer,
    'Mix3',
    imageDirectory,
    "Bach",
    directorystyle,
    composer)
CentralitiesScatterPlot(
    Bach,
    Directory,
    Composer,
    'Mix4',
    imageDirectory,
    "Bach",
    directorystyle,
    composer)
CentralitiesScatterPlot(
    Bach,
    Directory,
    Composer,
    'Eigenvalues',
    imageDirectory,
    "Bach",
    directorystyle,
    composer)
CentralitiesScatterPlot(
    Bach,
    Directory,
    Composer,
    'Closeness',
    imageDirectory,
    "Bach",
    directorystyle,
    composer)

print("The max is : ", getPiecesOutOfDistribution(Bach))
print("The max is : ", getPiecesOutOfDistribution(Directory))
print("The max is : ", getPiecesOutOfDistribution(Composer))

print("Comparison between Bach and " + directory +
      " : ", twoDictsDistCompare(Bach, Directory))
print("Comparison between Bach and ", composer +
      " : ", twoDictsDistCompare(Bach, Composer))
print(
    "Comparison between " +
    composer +
    "and " +
    directory +
    " : ",
    twoDictsDistCompare(
        Composer,
        Directory))

print(" SortPiecesByDistances : ")
print(SortPiecesByDistances(Bach))
print(SortPiecesByDistances(Composer))
print(SortPiecesByDistances(Directory))
