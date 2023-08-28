from singleItem import updateWarehouseSingleItemYearly
from config import initDB

def updateWarehouseAllItems(dataDict):
    print("Calculating using Simple Average! Please wait...")
    for item in dataDict:
        records = dataDict.get(item).get("records")
        updateWarehouseSingleItemYearly(symbol=item, records=records)

    print("Calculating using Weighted Average! Please wait...")


def main():
    db = initDB("./database.json")
    dataAsDictionary = db.get_all()
    updateWarehouseAllItems(dataAsDictionary)
    print("Yearly calculation done for all symbols. Database updated sucssfully!")


main();


