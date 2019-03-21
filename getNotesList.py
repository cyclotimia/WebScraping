import requests

url = "https://www.fragrantica.ru/perfume/Chanel/Chanel-No-5-Parfum-28711.html"

# ф-я, которая по урлу выдает список нот с их порядковым номером
def getNotesList(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    pageText = requests.get(url.split("\n")[0], headers=headers).text
    nl = pageText.split('" id="userMainNotes"')[0].split('Основные слышимые ноты по мнению пользователей')[1].split(
        'title="')[1]
    nl = nl.split(";")

    notesList = []
    weightsList = []

    for pair in nl:
        pair = pair.split(":")
        noteUrl = "https://www.fragrantica.ru/notes/note-" + pair[0] + ".html"
        noteName = \
            requests.get(noteUrl.split("\n")[0], headers=headers).text.split('<title>')[1].split('</title>')[0].split(
                " ингредиент аромата")[0]
        weightsList.append(int(pair[1]))
        notesList.append(noteName)

    weightMax = weightsList[0]
    percentage = []
    for weight in weightsList:
        noteWeight = weight / weightMax
        percentage.append(noteWeight)

    orderedNotesList = []
    l = len(notesList)

    for i in range (l):
        noteWithOrder = (notesList[i], percentage[i])
        orderedNotesList.append(noteWithOrder)

    return orderedNotesList

print(getNotesList(url))
