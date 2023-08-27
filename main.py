from pysondb import PysonDB
from singleItem import calculateSingleItem

def calculateAllItems(dataDict):
    for item in dataDict:
        records = dataDict.get(item).get("records")
        calculateSingleItem(item, records)


def main():
    db = PysonDB("./database.json")
    dataAsDictionary = db.get_all()
    calculateAllItems(dataAsDictionary)


main();


