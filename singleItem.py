from config import AppConfig
from pysondb import PysonDB
from datetime import datetime


def initWarehouse():
    warehouse = PysonDB("./warehouse.json")
    return warehouse
    

def calculateSingleItemYearly(symbol, records, strategy):
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
        yearSize = 365
        yearRangeCheck = fromYear >= AppConfig["StartYear"] and fromYear <= AppConfig["EndYear"] and toYear >= AppConfig["StartYear"] and toYear <= AppConfig["EndYear"]
        
        if not yearRangeCheck:
            continue
        # if covers diff years
        if fromYear != toYear:
            if fromYear%4 == 0:
                yearSize = 366
                toDay += yearSize
            else:
                toDay +=yearSize

        simpleRaisePerDay = priceRaisePercentage / (toDay - fromDay + 1)
        

        if fromYear == toYear:
            for dayIndex in range(fromDay, (toDay+1)):
                weightMap[fromYear][dayIndex-1] = simpleRaisePerDay
        elif fromYear < toYear:
            for dayIndex in range(fromDay, (toDay+1)):
                if dayIndex > yearSize:
                    dayIndex -= yearSize
                    weightMap[toYear][dayIndex-1] = simpleRaisePerDay
                else:
                    weightMap[fromYear][dayIndex-1] = simpleRaisePerDay 
        else:
            print("Data Error!! fromYear is greater than toYear!")
            
    print(weightMap)
    warehouse = initWarehouse()
    for year in weightMap:
        newRisingRate = {
            "symbol": symbol,
            "year": year,
            "risingRate": weightMap[year]
        }
        warehouse.add(newRisingRate)