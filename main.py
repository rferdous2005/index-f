from pysondb import PysonDB
from singleItem import calculateSingleItemYearly

def calculateAllItems(dataDict):
    print("Calculating using Simple Average! Please wait...")
    for item in dataDict:
        records = dataDict.get(item).get("records")
        calculateSingleItemYearly(symbol=item, records=records, strategy="simple")

    print("Calculating using Weighted Average! Please wait...")


def main():
    db = PysonDB("./database.json")
    dataAsDictionary = db.get_all()
    calculateAllItems(dataAsDictionary)
    print("Yearly calculation done for all symbols. Database updated!")


main();


