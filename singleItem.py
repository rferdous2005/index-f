from config import AppConfig
from pysondb import PysonDB
from datetime import datetime


def initWarehouse():
    warehouse = PysonDB("./warehouse.json")
    

def calculateSingleItem(symbol, records):
    weightMap = { }
    for year in range(AppConfig['StartYear'], AppConfig['EndYear']+1):
        weightMap[year] = [0.0]*366
    #print(weightMap)
    upTrends = records.get("up")
    downTrends = records.get("down")
    
    for upTrend in upTrends:
        fromObj = datetime.strptime(upTrend["fromDate"], "%d-%m-%Y")
        toObj = datetime.strptime(upTrend["toDate"], "%d-%m-%Y")
        fromDay = int(fromObj.strftime("%j"))
        toDay = int(toObj.strftime("%j"))
        fromYear = int(fromObj.strftime("%Y"))
        toYear = int(toObj.strftime("%Y"))
        priceRaisePercentage = (upTrend['toPrice']-upTrend["fromPrice"])*100/(upTrend["fromPrice"])

        # if covers diff years
        if fromYear != toYear:
            if fromYear%4 == 0:
                toDay += 366
            else:
                toDay +=365

        simpleRaisePerDay = priceRaisePercentage / (toDay - fromDay + 1)
        print(fromDay, fromYear, toDay, toYear, priceRaisePercentage, simpleRaisePerDay)