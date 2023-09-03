import matplotlib.pyplot as plt
from config import initDB, YearDateLabels
import numpy as np
from datetime import datetime



def q(data):
    if data['year']==2021 and data["symbol"]=="AIL":
        return True

warehouse = initDB(file="./warehouse.json")
filtered = warehouse.get_by_query(q)
filtered = list(filtered.values())[0]
d = datetime.strptime("29-02-2020", "%d-%m-%Y").strftime("%j")
print(d)
xpoints = np.array(YearDateLabels)
ypoints = np.array(filtered["risingRate"])

plt.plot(xpoints, ypoints)
plt.show()
#createDateLabels()