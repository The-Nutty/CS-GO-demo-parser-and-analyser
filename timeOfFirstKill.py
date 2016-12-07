import numpy as np
import matplotlib.pyplot as plt
from pymongo import MongoClient

plt.rcdefaults()

client = MongoClient()
collection = client.db.games

items = collection.find()#{"event": "2410"}
client.close()

timesWin = []
timesLoss = []

for i in items:
    for half in i["halfs"]:
        for thisRound in half:
            team1Time = 0#time of team1s first kill
            team2Time = 0
            if len(thisRound["team1Deaths"]) > 0:
                team2Time = thisRound["team1Deaths"][0]["time"]
                if team2Time > 400:
                    pass

            if len(thisRound["team2Deaths"]) > 0:
                team1Time = thisRound["team2Deaths"][0]["time"]
                if team1Time > 400:
                    pass

            if thisRound["winner"] == 1:
                timesWin.append(team1Time)
                if team2Time != 0:
                    timesLoss.append(team2Time)

            elif thisRound["winner"] == 2:
                timesWin.append(team2Time)
                if team1Time != 0:
                    timesLoss.append(team1Time)

plt.hist(timesWin, 50, normed=1, facecolor='green', alpha=0.75)
plt.hist(timesLoss, 50, normed=1, facecolor='red', alpha=0.75)
plt.title("Hits")

plt.show()