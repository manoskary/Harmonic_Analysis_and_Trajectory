
# x = 4, y = 3
NotePointsT345 = {
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

# x = 8, y = 3
NotePointsT138 = {
	0 : (0,0),
	1 : (2,3),
	2 : (1,2),
	3 : (0,1),
	4 : (2,0),
	5 : (1,3),
	6 : (0,2),
	7 : (2,1),
	8 : (1,0),
	9 : (0,3),
	10 : (2,2),
	11 : (1,1)
}

# x = 2, y = 9
NotePointsT129 = {
	0 : (0,0),
	1 : (2,1),
	2 : (1,0),
	3 : (0,3),
	4 : (2,0),
	5 : (1,3),
	6 : (0,2),
	7 : (2,3),
	8 : (1,2),
	9 : (0,1),
	10 : (2,2),
	11 : (1,1)
}

# x = 4, y = 1
NotePointsT147 = {
	0 : (0,0),
	1 : (0,1),
	2 : (0,2),
	3 : (0,3),
	4 : (1,0),
	5 : (1,1),
	6 : (1,2),
	7 : (1,3),
	8 : (2,0),
	9 : (2,1),
	10 : (2,2),
	11 : (2,3)
}

# x = 2, y = 3
NotePointsT237 = {
	0 : (0,0),
	1 : (2,3),
	2 : (1,0),
	3 : (0,1),
	4 : (2,0),
	5 : (1,1),
	6 : (0,2),
	7 : (2,1),
	8 : (1,2),
	9 : (0,3),
	10 : (2,2),
	11 : (1,3)
}


dictOfTonnetz = {
	'T345' : NotePointsT345,
	'T147' : NotePointsT147,
	'T138' : NotePointsT138,
	'T237' : NotePointsT237,
	'T129' : NotePointsT129
}


def PlaceFirstNote(listOfChords, Tonnetz):
	if Tonnetz == [3, 4, 5] :
		firstnote = listOfChords[0][0]
		position = NotePointsT345[firstnote]
	elif Tonnetz == [1, 3, 8] :
		firstnote = listOfChords[0][0]
		position = NotePointsT138[firstnote]
	elif Tonnetz == [1, 4, 7] :
		firstnote = listOfChords[0][0]
		position = NotePointsT147[firstnote]
	elif Tonnetz == [1, 2, 9] :
		firstnote = listOfChords[0][0]
		position = NotePointsT129[firstnote]
	elif Tonnetz == [2, 3, 7] :
		firstnote = listOfChords[0][0]
		position = NotePointsT237[firstnote]
	else :
		position = (0,0)
	return position
