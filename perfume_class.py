# парфюм
perfume = {
    "Brand": [],
    "Name": [],
    "Year": [],
    "Author": [],
    "Notes": [],
    "perfume_id": [],
}




class Perfume:
    def __init__(self, brand, name):
        self.brand = brand
        self.name = name
        self.year = 0
        self.authors = []
        self.perfume_id = ""
        self.notes = []

    def getName(self):
        return self.name

    def getBrand(self):
        return self.brand

    def getYear(self):
        return self.year

    def getAuthors(self):
        return self.authors

    def getId(self):
        return self.perfume_id

    def getNotes(self):
        return self.notes

    def perfumeToDict(self):
        perfume = {
            "Brand": self.brand,
            "Name": self.name,
            "Year": self.year,
            "Authors": self.authors,
            "Notes": self.notes,
            "perfume_id": self.perfume_id,
        }
        return perfume



thisPerf = Perfume("Chanel", "Chance")
thisPerf.year = 2006
thisPerf.authors=['Shyamala Maisondieu']
print(thisPerf.perfumeToDict())