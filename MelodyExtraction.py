from Tonnetz_Select import *
from FirstNotePosition import *
from TrajectoryCalculationsWithClass import *

def parseMF(midifile) :
	melody = []
	melodyTemp = []
	mfile = ms.converter.parse(midifile)
	mChords = mfile.chordify()
	for chord in mChords.recurse().getElementsByClass('Chord'):
		melodyTemp.append(max([p.midi for p in chord.pitches]))
	for index, note in enumerate(melodyTemp) :
		if index == 0 :
			pitchObj = ms.pitch.Pitch(note)
			melody.append(pitchObj.pitchClass)
		if index > 0:
			if note >= melodyTemp[index-1] - 12 :
				pitchObj = ms.pitch.Pitch(note)
				melody.append(pitchObj.pitchClass)
	return melody

def parseCorpus(file) :
	melody = []
	melodyTemp = []
	mChords = file.chordify()
	for chord in mChords.recurse().getElementsByClass('Chord'):
		melodyTemp.append(max([p.midi for p in chord.pitches]))
	for index, note in enumerate(melodyTemp) :
		if index == 0 :
			pitchObj = ms.pitch.Pitch(note)
			melody.append(pitchObj.pitchClass)
		if index > 0:
			if note >= melodyTemp[index-1] - 12 :
				pitchObj = ms.pitch.Pitch(note)
				melody.append(pitchObj.pitchClass)
	return melody

def removeDoubles(melodyPC) :
	newMelody = []
	for index, note in enumerate(melodyPC) :
		if index == 0 :
			newMelody.append(note)
		elif note != melodyPC[index-1] :
			newMelody.append(note)
	return newMelody

def findTonnetz(melody) :
	listOfTuples = []
	sequenceLength = 4
	for index, note in enumerate(melody) :
		if index <= len(melody) - sequenceLength :
			listOfTuples.append([note, melody[index+1], melody[index+2], melody[index+3]])

	intervalVectors = []
	for PC in listOfTuples :
		chord = ms.chord.Chord(PC)
		intervalVectors.append(chord.intervalVector)
	Tonnetz = TonnetzConfigDict(TonnetzConnectivity(intervalVectors))

	return listOfTuples, Tonnetz

def melodyTonnetzCorpus(file):
	melody = removeDoubles(parseCorpus(file))
	melodySeq, Tonnetz = findTonnetz(melody)
	return Tonnetz

def melodyTrajectory(midifile) :
	melody = removeDoubles(parseMF(midifile))
	melodySeq, Tonnetz = findTonnetz(melody)
# TODO   --    Define a new trajectory for melody
	trajectory = NewTrajectory(melodySeq, Tonnetz, PlaceFirstNote(melodySeq, Tonnetz))
	return trajectory





