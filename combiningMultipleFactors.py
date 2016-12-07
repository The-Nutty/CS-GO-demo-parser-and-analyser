import csv

import numpy as np
import matplotlib.pyplot as plt
from pymongo import MongoClient


nades = ["incgrenade", "molotov", "decoy", "smokegrenade", "flashbang", "hegrenade"]
client = MongoClient()
collection = client.db.games

items = collection.find()#{"event": "2410"}
client.close()

# 3 factors, collect win rate with each or none, less Hits, more shots, more nades
#[wins, losses]
zero = 0
one = 0
two = 0
three = 0

winningTeamNadeDiff = []#TODO:Fine what % when 0, 1 or 2 are won/lost
winningTeamShotDiff = []
winningTeamHitDiff = []
guns = []

ccvs = []
ccvs.append(["We Won", "less Hits", "More Shots", "More Nades"])

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

            firedMoreShots = False
            hitLessShots = False
            threwMoreNades = False

            hitDiff = team1Hits - team2Hits
            shotDiff = team1Shots - team2Shots
            nadeDiff = team1Nades - team2Nades
            # 3 factors, collect win rate with each or none, less Hits, more shots, more nades
            #if we won, hitdiff smaller, shotdiff larger, nade diff larger
            vals = [thisRound["winner"] == 1, True if hitDiff < 0 else False, True if shotDiff > 0 else False, True if nadeDiff > 0 else False]
            ccvs.append(vals)


with open('multaple.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

    for c in ccvs:
        spamwriter.writerow(c)
