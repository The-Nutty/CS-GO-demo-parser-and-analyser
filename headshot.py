import csv

import numpy as np
import matplotlib.pyplot as plt
from pymongo import MongoClient

plt.rcdefaults()

client = MongoClient()
collection = client.db.games

items = collection.find()
client.close()

winnerFirstKill = 0
losserFirstKill = 0

higherhs = 0
nokills = 0
lowerhs = 0

hsDiff = []

for i in items:
    for half in i["halfs"]:
        for thisRound in half:
            team1KillsHead = 0
            team1Kills = 0

            team2KillsHead = 0
            team2Kills = 0

            if len(thisRound["team1Deaths"]) > 0:
                for kill in thisRound["team1Deaths"]:
                    if kill["headShot"] == "1 ":
                        team2KillsHead += 1
                    else:
                        team2Kills += 1

            if len(thisRound["team2Deaths"]) > 0:
                for kill in thisRound["team2Deaths"]:
                    if kill["headShot"] == "1 ":
                        team1KillsHead += 1
                    else:
                        team1Kills += 1

            try:
                team2Ratio = team2KillsHead / (team2Kills + team2KillsHead)
            except:
                pass

            try:
                team1Ratio = team1KillsHead / (team1Kills + team1KillsHead)
            except:
                pass

            if thisRound["winner"] == 1:
                if team2Kills + team2KillsHead == 0:
                    nokills += 1
                elif team1Ratio > team2Ratio:
                    higherhs +=1
                else:
                    lowerhs += 1
                hsDiff.append([team1Ratio - team2Ratio, True, 1])

            elif thisRound["winner"] == 2:
                if team1Kills + team1KillsHead == 0:
                    nokills += 1
                elif team2Ratio > team1Ratio:
                    higherhs +=1
                else:
                    lowerhs += 1
                hsDiff.append([team1Ratio - team2Ratio, False, 1])

print(higherhs)
print(lowerhs)
print(nokills)

with open('hs.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(["Difference in headshot ratio", "Win", "val"])
    for c in hsDiff:
        spamwriter.writerow(c)

# n, bins, patches = plt.hist(hsDiff, 100, normed=1, facecolor='green', alpha=0.75)
# plt.title("Hits")
#
# plt.show()



# lowestShots = -1
# highestShots = -1
#
# for i in winningTeamDiff:
#     if lowestShots > i:
#         lowestShots = i
#     if highestShots < i:
#         highestShots = i
#
# interval = (highestShots - lowestShots) / SECTIONS
#
# winningTeamDiff.sort()
#
# values = {}
# lables = []
#
# for j in range(len(winningTeamDiff)):
#     if winningTeamDiff[j] in values:
#         values[winningTeamDiff[j]] += 1
#     else:
#         values[winningTeamDiff[j]] = 1
#
# # this is for scatter
# x = []
# y = []
# for key, value in values.items():
#     x.append(key)
#     y.append(value)
#
# moreNades = 0
# lessNades = 0
# for i in winningTeamDiff:
#     if i > 0:
#         moreNades += 1
#     elif i < 0:
#         lessNades += 1
#
# print(moreNades, lessNades)
#
# # # histagram stuff
# # n, bins, patches = plt.hist(winningTeamDiff, 100, normed=1, facecolor='green', alpha=0.75)
# # plt.title("Difference in grenades thrown between the winning team and the loosing team")
# #
# # plt.show()