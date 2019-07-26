# Harmonic_Analysis_and_Trajectory Repository

Introduction
=====================

A Notebook repository for Automated Harmonic Analysis of symbolic music data files with topological tools and graphs.

This is the work of my internship during the period 23/04 - 31/07 2019. It focuses on the creation of the harmonic fingerprint of musical scores in any symbolic form(mid, xml, mxl, krn, abc, etc.). 

We define a trajectory in a infinite Tonnetz Space for ref see (Tranformational Music Theory). We automatically choose the appropriate Tonnetz any piece analysed and we build its trajectory in a ZxZ cartesian plane.

We then define a Graph structure and apply Machine Learning for style, composer or other feature Prediction.


Software dependencies
=====================
<!-- Python Jupyter-Notebook modules : -->

This project is realized entirely in python and below you can find the packages used.

### Dependencies Python Packages:
* music21
* networkx
* matplotlib
* scipy
* numpy
* jupyter
* heapq_max
* scikit-learn
* pandas

Python related dependencies can be installed using:
```
  $ pip install -r requirements.txt
```
use pip for python 2 & pip3 for python 3

Few Results. . .
=====================

Binary Classification average over 8 classes : f1 score = 0.85


Some Directions
=====================

### Tonnetz_select.py

See how to parse Midi, xml or other data. It is the function that parses a file extracts and modifies the chords 
as PC-Sets and computes the appropriate Tonnetz.

### TrajectoryCalculationWithClass.py

This is the script that effectuates the computation of the trajectory in the Tonnetz Space. There are a few different definitions inside.
Trajectory is an object defined in "TrajectoryClass.py". The critical value of the Trajectory, among others, is a list of dictionaries of chords with keys the Pitch Class names of the notes and values 2 dimensional integer cordinates in the cartesian plane.

### graph_creation.py

A script that receives a Trajectory object and returns a complete graph object that includes trajectory with additional information about centralities, midiInfo, etc. The graph object is defined in "GraphClass.py"


