import requests, re, time
from random import randint

# список урлов
accountUrl = "https://www.fragrantica.ru/chlen/107129/"
delaymin = 400
delaymax = 1000
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
# парфюм
perfume = {
    "Brand": [],
    "Name": [],
    "Year": [],
    "Author": [],
    "Notes": [],
    "perfume_id": [],
}

def noteListSorter(list):
  finalNotes = {}

  for item in list:
    note = item[0]
    value = float(item[1])
    if note in finalNotes.keys():
      currentValue = finalNotes[note]
      newValue = currentValue + value
      finalNotes[note] = newValue
    else:
      finalNotes[note] = value

  import operator
  sortedNotes = sorted(finalNotes.items(), key=operator.itemgetter(1))

  return sortedNotes

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

# ф-я, которая принимает урл личного кабинета и выдает список урлов парфюмов
def getFavList(url):
    if "chlen" not in url:
        print("The given link is not a Fragrantica user profile link")
        return []

    favList = []

    pageText = requests.get(url.split("\n")[0], headers=headers).text

    searchArea = pageText.split('<div id="wardrobe">')[1].split('Популярные бренды и ароматы')[0]

    links = searchArea.split('<a href="/perfume/')

    l = len(links)
    urlsample = "https://www.fragrantica.ru/perfume/"
    for i in range(1, l):
        favUrl = urlsample + links[i].split('"')[0]
        favList.append(favUrl)

    return favList


# ф-я, которая по урлу выдает парфюм с заполненными полями
def getPerfume(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    perfumeNotes = []

    pageText = requests.get(url.split("\n")[0], headers=headers).text

    # берем perfume_id
    perfume_id = pageText.split("perfume_id:")[1].split(":")[0]

    # берем кусок текста html страницы, содержащий бренд и название
    perfumeBrandName = pageText.split('Бренды</a>')[1]
    perfumeBrandName = perfumeBrandName.split('</h1>')[0]
    # print("perfumeBrandName = ", perfumeBrandName)
    brand = perfumeBrandName.split('itemprop="name">')[1].split('</span>')[0]
    name = perfumeBrandName.split('itemprop="name">')[2].split(" " + brand)[0]

    # находим в тексте год выпуска
    year = []
    if '</b> выпущен в ' in pageText:
        findYear = pageText.split('</b> выпущен в ')
        yearLen = len(findYear)
        year = findYear[yearLen - 1].split('.')[0].split(' ')[0]
    elif '</b> создан в ' in pageText:
        year = pageText.split('</b> создан в ')[1].split(' ')[0]
    else:
        yMask = '\d\d\d\d'
        pageTitle = pageText.split("<title>")[1].split("</title>")[0]
        if re.search(yMask, pageTitle):
            year = pageTitle[-4:]

    # находим в тексте список парфюмеров
    perfumers = []
    listOfPerf = pageText.split('a href="https://www.fragrantica.ru/noses/')
    noOfPerf = len(listOfPerf) - 1
    if noOfPerf > 0:
        for i in range(1, noOfPerf + 1):
            thisPerfumer = listOfPerf[i].split(".html")[0]
            perfumers.append((thisPerfumer))

    # берем ноты и сохраняем в список

    perfumeNotes = getNotesList(url)

    # передаем все это в сущность perfume
    perfume["Brand"] = brand
    perfume["Name"] = name
    perfume["Year"] = year
    perfume["Author"] = perfumers
    perfume["Notes"] = perfumeNotes
    perfume["perfume_id"] = perfume_id

    # возвращаем perfume с заполненными полями
    return perfume


# функция печатаем и пишем ноты в файл
def writeNotes(url, list):
    try:
        thisPerfume = getPerfume(url)
        print("Perfume ID: ", thisPerfume["perfume_id"])
        print("Brand: ", thisPerfume["Brand"])
        print("Name: ", thisPerfume["Name"])
        perfumers = thisPerfume["Author"]
        print("Authors: ", thisPerfume["Author"])
        print("Year: ", thisPerfume["Year"])
        notes = thisPerfume["Notes"]
        print("Notes: ", notes)
        # переносим ноты в файл для статистики
        with open("notes.txt", "a") as myfile:
            for note in notes:
                myfile.write(note[0] + ":" + str(note[1]) + "\n")
                list.append(note)
        with open("authors.txt", "a") as myfile2:
            for person in perfumers:
                myfile2.write(person + "\n")

        print()
    except:
        pass

    return list
#
#
# основная функция - берем урлы и выдергиваем данные

# открываем очищаем файл
with open("notes.txt", "w") as notesfile:
    notesfile.write("")
with open("authors.txt", "w") as authors:
    authors.write("")

# парсим лист урлов парфюмов
urls = getFavList(accountUrl)
grandList = []
# парсим данные о парфюмах
for url in urls:
    resp = requests.get(url, headers=headers).status_code
    if resp == 429:
        delay = randint(delaymin, delaymax)
        print("sleeping for ", delay, " seconds...", "\n")
        time.sleep(delay)
        writeNotes(url, grandList)
    elif resp == 200:
        writeNotes(url, grandList)
    else:
        continue


print(noteListSorter(grandList))