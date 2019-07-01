from AutoHarmonicAnalysis import BachTrajectoryGraphs, GetWorksByComposer, GetWorksByDirectory
from PlottingGraphCentrality import CentralitiesScatterPlot, Centralities2DPlot

Bach = BachTrajectoryGraphs(200)
Directory = GetWorksByDirectory(input("Enter a Directory: "))
Composer = GetWorksByComposer(input("Enter A Composer's Name : "))

CentralitiesScatterPlot(Bach, Directory, Composer)