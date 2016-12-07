import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from pymongo import MongoClient
"""http://datascience.stackexchange.com/questions/6084/how-do-i-create-a-complex-radar-chart from"""
def _invert(x, limits):
    """inverts a value x on a scale from
    limits[0] to limits[1]"""
    return limits[1] - (x - limits[0])


def _scale_data(data, ranges):
    """scales data[1:] to ranges[0],
    inverts if the scale is reversed"""
    for d, (y1, y2) in zip(data[1:], ranges[1:]):
        assert (y1 <= d <= y2) or (y2 <= d <= y1)
    x1, x2 = ranges[0]
    d = data[0]
    if x1 > x2:
        d = _invert(d, (x1, x2))
        x1, x2 = x2, x1
    sdata = [d]
    for d, (y1, y2) in zip(data[1:], ranges[1:]):
        if y1 > y2:
            d = _invert(d, (y1, y2))
            y1, y2 = y2, y1
        sdata.append((d - y1) / (y2 - y1)
                     * (x2 - x1) + x1)
    return sdata


class ComplexRadar():
    def __init__(self, fig, variables, ranges,
                 n_ordinate_levels=6):
        angles = np.arange(0, 360, 360. / len(variables))

        axes = [fig.add_axes([0.1, 0.1, 0.9, 0.9], polar=True,
                             label="axes{}".format(i))
                for i in range(len(variables))]
        l, text = axes[0].set_thetagrids(angles,
                                         labels=variables)
        [txt.set_rotation(angle - 90) for txt, angle
         in zip(text, angles)]
        for ax in axes[1:]:
            ax.patch.set_visible(False)
            ax.grid("off")
            ax.xaxis.set_visible(False)
        for i, ax in enumerate(axes):
            # grid = np.linspace(*ranges[i],
            #                    num=n_ordinate_levels)
            grid = [0.1,10,20,30,40,50,60,70,80,90,100]
            gridlabel = ["{}".format(round(x, 2))
                         for x in grid]
            if ranges[i][0] > ranges[i][1]:
                grid = grid[::-1]  # hack to invert grid
                # gridlabels aren't reversed
            gridlabel[0] = ""  # clean up origin
            ax.set_rgrids(grid, labels=gridlabel,
                          angle=angles[i])
            # ax.spines["polar"].set_visible(False)
            ax.set_ylim(*ranges[i])
        # variables for plotting
        self.angle = np.deg2rad(np.r_[angles, angles[0]])
        self.ranges = ranges
        self.ax = axes[0]

    def plot(self, data, *args, **kw):
        sdata = _scale_data(data, self.ranges)
        self.ax.plot(self.angle, np.r_[sdata, sdata[0]], *args, **kw)

    def fill(self, data, *args, **kw):
        sdata = _scale_data(data, self.ranges)
        self.ax.fill(self.angle, np.r_[sdata, sdata[0]], *args, **kw)


# TODO:

nades = ["incgrenade", "molotov", "decoy", "smokegrenade", "flashbang", "hegrenade"]
client = MongoClient()
collection = client.db.games

items = collection.find({"event": "2410"})
client.close()

winningTeamNadeDiff = []
winningTeamShotDiff = []
winningTeamHitDiff = []
guns = []

winnerFirstKill = 0
losserFirstKill = 0

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

            #First kill ralted stuff
            team1Time = 99  # the time a first palyer from team 1 died
            team2Time = 99  # the time a first palyer from team 2 died

            if len(thisRound["team1Deaths"]) > 0:
                team1Time = thisRound["team1Deaths"][0]["time"]

            if len(thisRound["team2Deaths"]) > 0:
                team2Time = thisRound["team2Deaths"][0]["time"]

            if thisRound["winner"] == 1:
                if team2Time < team1Time:
                    winnerFirstKill += 1
                else:
                    losserFirstKill += 1

            elif thisRound["winner"] == 2:
                if team2Time > team1Time:
                    winnerFirstKill += 1
                else:
                    losserFirstKill += 1

moreNades = 0
lessNades = 0
for i in winningTeamNadeDiff:
    if i > 0:
        moreNades += 1
    elif i < 0:
        lessNades += 1

moreShots = 0
lessShots = 0
for i in winningTeamShotDiff:
    if i > 0:
        moreShots += 1
    elif i < 0:
        lessShots += 1

moreHits = 0
lessHits = 0
for i in winningTeamHitDiff:
    if i > 0:
        moreHits += 1
    elif i < 0:
        lessHits += 1

# example data
variables = ("Nades", "Shots", "Hits", "First Kills")

print(moreHits, lessHits)

data = (moreNades / (lessNades + moreNades) * 100, moreShots / (lessShots + moreShots) * 100,
        moreHits / (lessHits + moreHits) * 100, winnerFirstKill / (losserFirstKill + winnerFirstKill) * 100)
ranges = [(0.1, 100), (0.1, 100), (0.1, 100), (0.1, 100)]

print(moreHits / (lessHits + moreHits) * 100)

# plotting
fig1 = plt.figure(figsize=(6, 6))
radar = ComplexRadar(fig1, variables, ranges)
radar.plot(data)
radar.fill(data, alpha=0.2)

plt.savefig("test.png",bbox_inches='tight')

plt.show()
