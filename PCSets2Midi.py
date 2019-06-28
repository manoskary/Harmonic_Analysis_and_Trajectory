from music21 import chord, midi, stream
import os.path


def PC2Midi(listOfChords, directory) :
	name_of_file = input("What is the name of the file: ")
	print("Please wait while process ...")
	completeName = os.path.join(directory, name_of_file+".mid") 
	file = open(completeName, "w")
	chordStream = stream.Stream()
	for c in listOfChords :
		chordObject = chord.Chord(c)
		chordObject.quarterLength = 1
		chordStream.append(chordObject)
	mf = midi.translate.streamToMidiFile(chordStream)
	mf.open(completeName, 'wb')
	mf.write()
	mf.close()