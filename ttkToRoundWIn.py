import csv

import numpy as np
import matplotlib.pyplot as plt
from pymongo import MongoClient

plt.rcdefaults()

client = MongoClient()
collection = client.db.games

items = collection.find({"event": "2410"})
client.close()

winnerFirstKill = 0
losserFirstKill = 0

higherhs = 0
nokills = 0
lowerhs = 0

win = []
loss = []

for i in items:
    for half in i["halfs"]:
        for thisRound in half:
            k = {}  # store for hte time of eatch kill
            h = {}  # store for hte first hit

            k1 = {}
            h1 = {}

            # do for team1 initlay
            for kill in thisRound["team2Deaths"]:
                k[kill["Player"]] = kill["time"]

            for hurt in thisRound["team2Hits"]:
                if hurt["PlayerHurt"] not in h or float(h[hurt["PlayerHurt"]]) > float(hurt["time"]):
                    h[hurt["PlayerHurt"]] = hurt["time"]


            for kill in thisRound["team1Deaths"]:
                k1[kill["Player"]] = kill["time"]

            for hurt in thisRound["team1Hits"]:
                if hurt["PlayerHurt"] not in h1 or float(h1[hurt["PlayerHurt"]]) > float(hurt["time"]):
                    h1[hurt["PlayerHurt"]] = hurt["time"]

            ttks = []
            for key, value in k.items():
                try:
                    ttks.append(float(value) - float(h[key]))
                except:
                    pass

            ttks1 = []
            for key, value in k1.items():
                try:
                    ttks.append(float(value) - float(h1[key]))
                except:
                    pass

            if thisRound["winner"] == 1:
                win += ttks
                loss += ttks1

            elif thisRound["winner"] == 2:
                loss += ttks
                win += ttks1

print(win)
print(loss)
print(len(win))
print(len(loss))

xLoss = []
yLoss = []

for i in range(500):
    count = 0
    for j in loss:
        if round(j) == i:
            count += 1
    if count > 0:
        xLoss.append(i)
        yLoss.append(count)

xWon = []
yWon = []

for i in range(500):
    count = 0
    for j in win:
        if round(j) == i:
            count += 1
    if count > 0:
        xWon.append(i)
        yWon.append(count)




# plt.hist(win, 200, normed=1, facecolor='green', alpha=0.75)
# plt.hist(loss, 200, normed=1, facecolor='red', alpha=0.75)
plt.scatter(xLoss, yLoss, color="red")
plt.scatter(xWon, yWon, color="green")
plt.title("Hits")

plt.show()

