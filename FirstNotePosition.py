

NotePoints = {
	0 : (0,0),
	1 : (1,3),
	2 : (2,2),
	3 : (0,1),
	4 : (1,0),
	5 : (2,3),
	6 : (0,2),
	7 : (1,1),
	8 : (2,0),
	9 : (0,3),
	10 : (1,2),
	11 : (2,1)
}

def PlaceFirstNote(listOfChords, Tonnetz):
	if Tonnetz == [3, 4, 5] :
		firstnote = listOfChords[0][0]
		position = NotePoints[firstnote]
	else :
		position = (0,0)
	return position
