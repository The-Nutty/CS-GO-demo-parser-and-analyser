import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from pymongo import MongoClient
import csv

nades = ["incgrenade", "molotov", "decoy", "smokegrenade", "flashbang", "hegrenade"]
client = MongoClient()
collection = client.db.games

items = collection.find()#{"event": "2410"}
client.close()

winningTeamNadeDiff = []
winningTeamShotDiff = []
winningTeamHitDiff = []
guns = []

winnerFirstKill = 0
losserFirstKill = 0

ccvs = []
ccvs.append(["First Kill diff", "Hits Diff", "Shots Diff", "Nades Diff", "Winner"])
for i in items:
    for half in i["halfs"]:
        for thisRound in half:
            team1Nades = 0
            team2Nades = 0

            team1Shots = 0
            team2Shots = 0

            team1Hits = 0
            team2Hits = 0
            for shot in thisRound["team1Shots"]:
                team1Shots += 1
                for nade in nades:
                    if nade in shot["gun"]:
                        team1Nades += 1

            for shot1 in thisRound["team2Shots"]:
                team2Shots += 1
                for nade in nades:
                    if nade in shot1["gun"]:
                        team2Nades += 1

            for hit in thisRound["team1Hits"]:
                team1Hits += 1

            for hit1 in thisRound["team2Hits"]:
                team2Hits += 1

            nadeDiff = 0
            shotDiff = 0
            hitDiff = 0
            if thisRound["winner"] == 1:
                hitDiff = team1Hits - team2Hits
                shotDiff = team1Shots - team2Shots
                nadeDiff = team1Nades - team2Nades
            elif thisRound["winner"] == 2:
                hitDiff = team2Hits - team1Hits
                shotDiff = team2Shots - team1Shots
                nadeDiff = team2Nades - team1Nades

            winningTeamNadeDiff.append(nadeDiff)
            winningTeamShotDiff.append(shotDiff)
            winningTeamHitDiff.append(hitDiff)

            # First kill ralted stuff
            if len(thisRound["team1Deaths"]) > 0:
                team1Time = thisRound["team1Deaths"][0]["time"]
            else:
                team1Time == 155#theretical max round time

            if len(thisRound["team2Deaths"]) > 0:
                team2Time = thisRound["team2Deaths"][0]["time"]
            else:
                team2Time == 155#theretical max round time

            roundStats = [team1Time - team2Time, team1Hits - team2Hits, team1Shots - team2Shots,
                          team1Nades - team2Nades]

            if thisRound["winner"] == 1:
                roundStats.append(True)
                if team2Time < team1Time:
                    winnerFirstKill += 1
                else:
                    losserFirstKill += 1

            elif thisRound["winner"] == 2:
                roundStats.append(False)
                if team2Time > team1Time:
                    winnerFirstKill += 1
                else:
                    losserFirstKill += 1
            ccvs.append(roundStats)

with open('rounds.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)

    for c in ccvs:
        spamwriter.writerow(c)
