import matplotlib.pyplot as plt
from config import initDB, AppConfig, YearDateLabels
import numpy as np
from datetime import datetime


def query(data):
    if data['year'] >= AppConfig["AverageFrom"] and data['year'] <= AppConfig["AverageTo"] and data["symbol"] in AppConfig["selectedSymbols"]:
        return True
    
def useSimpleAvg(queryList):
    finalWeightMap = {}
    countMap = {}
    
    for row in queryList:
        if row['symbol'] in finalWeightMap:
            countMap[row['symbol']] += 1
            finalWeightMap[row['symbol']] = np.sum([finalWeightMap[row['symbol']],row['risingRate']], axis=0) #sum list with list
            finalWeightMap[row['symbol']] = np.around(finalWeightMap[row['symbol']], 5) # rounding numbers in numpy array
        else:
            countMap[row['symbol']] = 1
            finalWeightMap[row['symbol']] = row['risingRate']
        #finalWeightMap[row['symbol']] = np.around(finalWeightMap[row['symbol']]*10, 3)
    for uniqueSymbol in finalWeightMap:
        finalWeightMap[uniqueSymbol] = np.around(finalWeightMap[uniqueSymbol]*10/countMap[uniqueSymbol], 3) # generalize with *10 & upto 3 decimals
        #print(uniqueSymbol, finalWeightMap[uniqueSymbol],len(finalWeightMap[uniqueSymbol]), countMap[uniqueSymbol])
        fromDate = datetime.strptime(AppConfig["StartDay"], "%d-%b")
        toDate = datetime.strptime(AppConfig["EndDay"], "%d-%b")
        fromDate = int(fromDate.strftime("%j"))
        toDate = int(toDate.strftime("%j"))
        dateLabels = YearDateLabels[fromDate-1:toDate]
        #print(len(dateLabels))
        #print(dateLabels)
        finalWeightMap[uniqueSymbol] = finalWeightMap[uniqueSymbol][fromDate-1:toDate]
        #print(len(finalWeightMap[uniqueSymbol]))
        #print(finalWeightMap[uniqueSymbol])
        plt.title("Symbol: "+uniqueSymbol+ " Using S.A. from "+ AppConfig["StartDay"]+" to "+ AppConfig["EndDay"])
        plt.scatter(dateLabels, finalWeightMap[uniqueSymbol])
        #plt.show()

def useWeightedAvg(queryList):
    finalWeightMap = {}
    countMap = {}
    #print(queryList)
    for row in queryList:
        yearlyWeight = row['year']-AppConfig["AverageFrom"]+1
        print(yearlyWeight)
        if row['symbol'] in finalWeightMap:
            countMap[row['symbol']] += yearlyWeight
            print(row['risingRate'])
            row['risingRate'] = row['risingRate']*yearlyWeight
            #print(finalWeightMap[row['symbol']],row['risingRate'], row['year'])
            print(row['risingRate'])
            finalWeightMap[row['symbol']] = np.sum([finalWeightMap[row['symbol']],row['risingRate']], axis=0) #sum list with list
            finalWeightMap[row['symbol']] = np.around(finalWeightMap[row['symbol']], 5) # rounding numbers in numpy array
        else:
            countMap[row['symbol']] = yearlyWeight
            finalWeightMap[row['symbol']] = row['risingRate']*yearlyWeight
        #finalWeightMap[row['symbol']] = np.around(finalWeightMap[row['symbol']]*10, 3)
    for uniqueSymbol in finalWeightMap:
        finalWeightMap[uniqueSymbol] = np.around(finalWeightMap[uniqueSymbol]*10/countMap[uniqueSymbol], 3) # generalize with *10 & upto 3 decimals
        #print(uniqueSymbol, finalWeightMap[uniqueSymbol],len(finalWeightMap[uniqueSymbol]), countMap[uniqueSymbol])
        fromDate = datetime.strptime(AppConfig["StartDay"], "%d-%b")
        toDate = datetime.strptime(AppConfig["EndDay"], "%d-%b")
        fromDate = int(fromDate.strftime("%j"))
        toDate = int(toDate.strftime("%j"))
        dateLabels = YearDateLabels[fromDate-1:toDate]
        #print(len(dateLabels))
        print(dateLabels)
        finalWeightMap[uniqueSymbol] = finalWeightMap[uniqueSymbol][fromDate-1:toDate]
        #print(len(finalWeightMap[uniqueSymbol]))
        print(finalWeightMap[uniqueSymbol])
        plt.title("Symbol: "+uniqueSymbol+ " Using W.A. from "+ AppConfig["StartDay"]+" to "+ AppConfig["EndDay"])
        plt.scatter(dateLabels, finalWeightMap[uniqueSymbol])
        plt.show()

def main():
    warehouse = initDB(file="./warehouse.json")
    filteredData = warehouse.get_by_query(query)
    filteredList = list(filteredData.values())
    #useSimpleAvg(queryList=filteredList)
    useWeightedAvg(queryList=filteredList)
    
        
    #print(filteredList)
    
main()