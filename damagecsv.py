import csv

import numpy as np
import matplotlib.pyplot as plt
from pymongo import MongoClient

plt.rcdefaults()

client = MongoClient()
collection = client.db.games

items = collection.find()
client.close()


rows = []
rows.append(["Dammage diff", "Win"])
for i in items:
    for half in i["halfs"]:
        for thisRound in half:
            team1dmg = 0
            team2dmg = 0

            for hurt in thisRound["team1Hits"]:
                try:
                    team2dmg += int(hurt["damage"])
                except:
                    pass

            for hurt in thisRound["team2Hits"]:
                try:
                    team1dmg += int(hurt["damage"])
                except:
                    pass

            if thisRound["winner"] == 1:
                rows.append([team1dmg - team2dmg, True])

            elif thisRound["winner"] == 2:
                rows.append([team1dmg - team2dmg, False])

# plt.hist(win, 200, normed=1, facecolor='green', alpha=0.75)
# plt.hist(loss, 200, normed=1, facecolor='red', alpha=0.75)
# # plt.scatter(x,y)
# plt.title("Hits")

# plt.show()

with open('dmg.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for c in rows:
        spamwriter.writerow(c)
