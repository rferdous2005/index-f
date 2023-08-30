from config import AppConfig, isLeapYear
from config import initDB
from datetime import datetime


def updateWarehouseSingleItemYearly(symbol, records):
    weightMap = { }
    for year in range(AppConfig['StartYear'], AppConfig['EndYear']+1):
        if isLeapYear(year=year):
            weightMap[year] = [0.0]*366
        else:
            weightMap[year] = [0.0]*365
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
        yearRangeCheck = (fromYear >= AppConfig["StartYear"] and fromYear <= AppConfig["EndYear"]) or (toYear >= AppConfig["StartYear"] and toYear <= AppConfig["EndYear"])
        print(fromDay, toDay, fromYear, toYear)
        print(isLeapYear(fromYear))
        if not yearRangeCheck:
            continue
        # if covers diff years
        if fromYear != toYear:
            if isLeapYear(fromYear):
                yearSize = 366
                toDay += yearSize
            else:
                toDay +=yearSize

        simpleRaisePerDay = priceRaisePercentage / (toDay - fromDay + 1)
        simpleRaisePerDay = round(simpleRaisePerDay, 5)

        if fromYear == toYear:
            for dayIndex in range(fromDay, (toDay+1)):
                weightMap[fromYear][dayIndex-1] = simpleRaisePerDay
        elif fromYear < toYear:
            print(fromDay, toDay, fromYear, toYear, yearSize)
            for dayIndex in range(fromDay, (toDay+1)):
                dayIndexCopy = dayIndex 
                if dayIndexCopy > yearSize:
                    if toYear > AppConfig["EndYear"]:
                        break
                    dayIndexCopy -= yearSize
                    weightMap[toYear][dayIndexCopy-1] = simpleRaisePerDay
                else:
                    #print(dayIndexCopy)
                    weightMap[fromYear][dayIndexCopy-1] = simpleRaisePerDay 
        else:
            print("Data Error!! fromYear is greater than toYear!")

    for downTrend in downTrends:
        fromObj = datetime.strptime(downTrend["fromDate"], "%d-%m-%Y")
        toObj = datetime.strptime(downTrend["toDate"], "%d-%m-%Y")
        fromDay = int(fromObj.strftime("%j"))
        toDay = int(toObj.strftime("%j"))
        fromYear = int(fromObj.strftime("%Y"))
        toYear = int(toObj.strftime("%Y"))
        priceRaisePercentage = (downTrend['toPrice']-downTrend["fromPrice"])*100/(downTrend["fromPrice"])
        yearSize = 365
        yearRangeCheck = (fromYear >= AppConfig["StartYear"] and fromYear <= AppConfig["EndYear"]) or (toYear >= AppConfig["StartYear"] and toYear <= AppConfig["EndYear"])
        print(fromDay, toDay, fromYear, toYear)
        print(isLeapYear(fromYear))
        if not yearRangeCheck:
            continue
        # if covers diff years
        if fromYear != toYear:
            if isLeapYear(fromYear):
                yearSize = 366
                toDay += yearSize
            else:
                toDay +=yearSize

        simpleRaisePerDay = priceRaisePercentage / (toDay - fromDay + 1)
        simpleRaisePerDay = round(simpleRaisePerDay, 5)

        if fromYear == toYear:
            for dayIndex in range(fromDay, (toDay+1)):
                weightMap[fromYear][dayIndex-1] = simpleRaisePerDay
        elif fromYear < toYear:
            print(fromDay, toDay, fromYear, toYear)
            for dayIndex in range(fromDay, (toDay+1)):
                dayIndexCopy = dayIndex 
                if dayIndexCopy > yearSize:
                    if toYear > AppConfig["EndYear"]:
                        break
                    dayIndexCopy -= yearSize
                    weightMap[toYear][dayIndexCopy-1] = simpleRaisePerDay
                else:
                    weightMap[fromYear][dayIndexCopy-1] = simpleRaisePerDay 
        else:
            print("Data Error!! fromYear is greater than toYear!")
            
    #print(weightMap)
    warehouse = initDB(file="./warehouse.json")
    for year in weightMap:
        newRisingRate = {
            "symbol": symbol,
            "year": year,
            "risingRate": weightMap[year]
        }
        warehouse.add(newRisingRate)