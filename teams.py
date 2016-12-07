import csv

import numpy as np
import matplotlib.pyplot as plt
from pymongo import MongoClient

plt.rcdefaults()

client = MongoClient()
collection = client.db.games

teams = collection.distinct("team1Name")
teams += collection.distinct("team2Name")
results = {}
# allCT = 0
# allT = 0
for team in teams:
    matches1 = collection.find({"team1Name" : team})
    matches2 = collection.find({"team2Name" : team})
    roundsWon = 0
    roundsLost = 0
    for mat in matches1:
        roundsWon += mat["team1Score"]
        roundsLost += mat["team2Score"]
    for mat in matches2:
        roundsWon += mat["team2Score"]
        roundsLost += mat["team1Score"]

    results[team] = [roundsWon/(roundsWon + roundsLost), roundsWon + roundsLost]

print(results)
with open('teams.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(["Team", "Win Ratio", "Rounds Played"])
    for key, value in results.items():
        spamwriter.writerow([key, value[0], value[1]])

client.close()
