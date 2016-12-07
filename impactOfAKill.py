import numpy as np
import matplotlib.pyplot as plt; plt.rcdefaults()
from pymongo import MongoClient

SECTIONS = 10

client = MongoClient()
collection = client.db.games

items = collection.find()#{"event": "2410"}

kills = {}

won = {}
lost = {}


def addTo(dict, death):
    if death["gun"] in dict:
        dict[death["gun"]] = dict[death["gun"]] + 1
    else:
        dict[death["gun"]] = 1


for i in items:
    for half in i["halfs"]:
        for thisRound in half:
            winner = thisRound["winner"]
            team1Shots = 0
            team2Shots = 0
            for death in thisRound["team1Deaths"]:
                if death["gun"] in kills:
                    kills[death["gun"]] = kills[death["gun"]] + 1
                else:
                    kills[death["gun"]] = 1

                if winner == 1:#lost
                    addTo(lost, death)
                elif winner == 2:#won
                    addTo(won, death)

            for death in thisRound["team2Deaths"]:
                if death["gun"] in kills:
                    kills[death["gun"]] = kills[death["gun"]] + 1
                else:
                    kills[death["gun"]] = 1

                if winner == 1:  # won
                    addTo(won, death)
                elif winner == 2:  # lost
                    addTo(lost, death)


            # diff = 0
            # if thisRound["winner"] == 1:
            #     diff = team1Shots - team2Shots
            # elif thisRound["winner"] == 2:
            #     diff = team2Shots - team1Shots
            #
            # winningTeamDiff.append(diff)


#//rounds won where you get a kill with a gun

combined = {}
for key, value in won.items():
    if key not in combined:
        w = won[key] if key in won else 0
        l = lost[key] if key in lost else 0
        combined[key] = w /(w + l)
for key, value in lost.items():
    if key not in combined:
        w = won[key] if key in won else 0
        l = lost[key] if key in lost else 0
        combined[key] = w /(w + l)

del combined[""]

for key, value in dict(combined).items():
    if "knife" in key:
        del combined[key]

print (combined)
x = []
y = []
count = 0
for key, value in combined.items():
    x.append(count)
    y.append(value)
    count += 1


plt.bar(x, y, 1/1.5,align='center')
plt.ylabel('Rounds')
plt.xticks(range(len(combined)), combined.keys())
plt.tight_layout()
plt.show()