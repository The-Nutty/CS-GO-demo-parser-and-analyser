import csv

import numpy as np
import matplotlib.pyplot as plt
from pymongo import MongoClient

plt.rcdefaults()

client = MongoClient()
collection = client.db.games

maps = collection.distinct("map")
results = {}
# allCT = 0
# allT = 0
for map in maps:
    matches = collection.find({"map" : map})
    CT = 0
    T = 0
    for mat in matches:
        isCt = True
        for half in mat["halfs"]:
            for thisRound in half:
                if (thisRound["winner"] == 1 and isCt) or (thisRound["winner"] == 2 and not isCt):
                    #CT won round
                    CT += 1
                else:
                    #T team won#
                    T += 1
            isCt = not isCt
    results[map] = [CT, T]

print(results)
with open('maps.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(["Map", "CT", "T", "Total"])
    for key, value in results.items():
        spamwriter.writerow([key, value[0]/(value[0] + value[1]) * 100, value[1]/(value[0] + value[1]) * 100, value[0] + value[1]])
















client.close()
