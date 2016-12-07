import numpy as np
import matplotlib.pyplot as plt
from pymongo import MongoClient

plt.rcdefaults()

SECTIONS = 10
nades = ["incgrenade", "molotov", "decoy", "smokegrenade", "flashbang", "hegrenade"]
client = MongoClient()
collection = client.db.games

items = collection.find({"event": "2410"})
client.close()

winningTeamDiff = []
guns = []

for i in items:
    for half in i["halfs"]:
        for thisRound in half:
            team1Nades = 0
            team2Nades = 0
            for shot in thisRound["team1Shots"]:
                for nade in nades:
                    if nade in shot["gun"]:
                        team1Nades += 1

            for shot1 in thisRound["team2Shots"]:
                for nade in nades:
                    if nade in shot1["gun"]:
                        team2Nades += 1

            diff = 0
            if thisRound["winner"] == 1:
                diff = team1Nades - team2Nades
            elif thisRound["winner"] == 2:
                diff = team2Nades - team1Nades

            winningTeamDiff.append(diff)

lowestShots = -1
highestShots = -1

for i in winningTeamDiff:
    if lowestShots > i:
        lowestShots = i
    if highestShots < i:
        highestShots = i

interval = (highestShots - lowestShots) / SECTIONS

winningTeamDiff.sort()

values = {}
lables = []

for j in range(len(winningTeamDiff)):
    if winningTeamDiff[j] in values:
        values[winningTeamDiff[j]] += 1
    else:
        values[winningTeamDiff[j]] = 1

# this is for scatter
x = []
y = []
for key, value in values.items():
    x.append(key)
    y.append(value)

moreNades = 0
lessNades = 0
for i in winningTeamDiff:
    if i > 0:
        moreNades += 1
    elif i < 0:
        lessNades += 1

print(moreNades, lessNades)

# histagram stuff
n, bins, patches = plt.hist(winningTeamDiff, 100, normed=1, facecolor='green', alpha=0.75)
plt.title("Difference in grenades thrown between the winning team and the loosing team")

plt.show()

