from operator import itemgetter

def topItems(noteslist, n): #noteslist = "notes.txt" например
    favNotes = []
    nn = []
    result = []
    with open(noteslist, "r") as myfile:
        favNotes = myfile.readlines()
        for note in favNotes:
            x = favNotes.count(note)
            if note not in nn:
                nn.append(note)
                result.append((note, x))
    return sorted(result, key=itemgetter(1))[-n:]

print("Top 10 preferred notes:", "\n")
print(topItems("notes.txt", 10))
print()
print("Top 5 preferred perfumers:", "\n")
print(topItems("authors.txt", 7))
