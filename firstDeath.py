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

for i in items:
    for half in i["halfs"]:
        for thisRound in half:
            team1Time = 99 #the time a first palyer from team 1 died
            team2Time = 99 #the time a first palyer from team 2 died

            if len(thisRound["team1Deaths"]) > 0:
                team1Time = thisRound["team1Deaths"][0]["time"]

            if len(thisRound["team2Deaths"]) > 0:
                team2Time = thisRound["team2Deaths"][0]["time"]

            if thisRound["winner"] == 1:
                if team2Time < team1Time:
                    winnerFirstKill +=1
                else:
                    losserFirstKill += 1

            elif thisRound["winner"] == 2:
                if team2Time > team1Time:
                    winnerFirstKill +=1
                else:
                    losserFirstKill += 1


print(winnerFirstKill)
print(losserFirstKill)