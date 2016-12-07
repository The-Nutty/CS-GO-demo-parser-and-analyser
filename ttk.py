import csv

import numpy as np
import matplotlib.pyplot as plt
from pymongo import MongoClient
import json

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

win = []
loss = []
more = 0
less = 0

x=[]
y=[]
for i in items:
    if i["team1Score"] > i["team2Score"]:
        x.append(i["team1Score"])
        y.append(i["team2Score"])
    else:
        x.append(i["team2Score"])
        y.append(i["team1Score"])


    # for half in i["halfs"]:
        # for thisRound in half:
            # k = {}  # store for hte time of eatch kill
            # h = {}  # store for hte first hit
            #
            # k1 = {}
            # h1 = {}
            #
            # # do for team1 initlay
            # for kill in thisRound["team2Deaths"]:
            #     k[kill["Player"]] = kill["time"]
            #
            # for hurt in thisRound["team2Hits"]:
            #     if hurt["PlayerHurt"] not in h or float(h[hurt["PlayerHurt"]]) > float(hurt["time"]):
            #         h[hurt["PlayerHurt"]] = hurt["time"]
            #
            #
            # for kill in thisRound["team1Deaths"]:
            #     k1[kill["Player"]] = kill["time"]
            #
            # for hurt in thisRound["team1Hits"]:
            #     if hurt["PlayerHurt"] not in h1 or float(h1[hurt["PlayerHurt"]]) > float(hurt["time"]):
            #         h1[hurt["PlayerHurt"]] = hurt["time"]
            #
            # ttk1 = []
            # for key, value in k.items():
            #     try:
            #         ttk1.append(float(value) - float(h[key]))
            #     except:
            #         pass
            #
            # ttk2 = []
            # for key, value in k1.items():
            #     try:
            #         ttk2.append(float(value) - float(h1[key]))
            #     except:
            #         pass
            # if len(ttk1) > 0:
            #     avg1 = sum(ttk1) / float(len(ttk1))
            # if len(ttk2) > 0:
            #     avg2 = sum(ttk2) / float(len(ttk2))


            # if thisRound["winner"] == 1:
            #     if ttk1 > ttk2:
            #         more += 1
            #     else:
            #         less += 1
            #
            # elif thisRound["winner"] == 2:
            #     if ttk1 < ttk2:
            #         more += 1
            #     else:
            #         less += 1

# print(more)
# print(less)

# xLoss = []
# yLoss = []
#
# for i in range(500):
#     count = 0
#     for j in loss:
#         if round(j) == i:
#             count += 1
#     if count > 0:
#         xLoss.append(i)
#         yLoss.append(count)
#
# xWon = []
# yWon = []
#
# for i in range(500):
#     count = 0
#     for j in win:
#         if round(j) == i:
#             count += 1
#     if count > 0:
#         xWon.append(i)
#         yWon.append(count)




# plt.hist(win, 200, normed=1, facecolor='green', alpha=0.75)
# plt.hist(loss, 200, normed=1, facecolor='red', alpha=0.75)
# plt.scatter(xLoss, yLoss, color="red")
plt.scatter(x, y, color="green")
plt.title("Hits")

plt.show()

