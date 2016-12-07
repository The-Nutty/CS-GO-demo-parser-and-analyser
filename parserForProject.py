import os
import os.path
import sys
import json

import gc
from pymongo import MongoClient

"""This works back and find the last tick and returns its tick number"""
"""For easy start to shorts fire vs win chance"""""


def findCurrentTick(i, content):
    tick = i
    while (not "CNETMsg_Tick" in content[tick]):
        tick = tick - 1
    return int(content[tick + 1][6:])


# produces json consisting of a list of halfs containing a list of rounds
def parseDemo(demoPath, eventId):
    if eventId != None:
        demoPath = "demos/" + eventId + "/" + demoPath
    else:
        demoPath = "demos/" + demoPath

    print("Parsing Demo " + demoPath)

    # if a demo exists parse it using demoinfogo
    if os.path.isfile(demoPath):
        os.system("demoinfogo.exe " + demoPath + " > demo.txt")
    else:
        print(demoPath + " not found, Skipping")
        return

    print("Demo parsed using demoinfogo")

    # read the whole string in to ram (It will be worth doing some kind of buffering in the future) latin-1 encoding is required for some reason..
    with open("demo.txt", encoding="latin-1") as f:
        content = f.read().splitlines()
    team1Shots = []  # team that starts CT
    team2Shots = []
    team1Deaths = []
    team2Deaths = []

    team1Hits = []
    team2Hits = []

    team1Name = None
    team2Name = None
    teamMultiplyer = True
    warmUpEnded = False
    team1Score = 0
    team2Score = 0
    scoreFlipFlop = True
    # tick rate related stuff
    tickInterval = -1  # tick rate of server
    tickOfRoundStart = -1
    # Json stuff:
    jsonData = {}
    halfs = []
    rounds = []
    round = {}
    for i in range(len(content)):
        currentLine = content[i]

        # stringtable stuff: used to get team names
        if "m_szClanTeamname" in currentLine and ((team2Name == None) or (team1Name == None)):
            teamName = content[i - 1][25:]
            if teamName == "TERRORIST":
                team2Name = currentLine[29:]
                jsonData["team2Name"] = currentLine[29:]
            elif teamName == "CT":
                team1Name = currentLine[29:]
                jsonData["team1Name"] = currentLine[29:]

        # stringTable stuff get tick rate
        elif "tick_interval:" in currentLine:
            tickInterval = float(currentLine[15:])

        # string table stuff: get map name
        elif "map_name:" in currentLine:
            jsonData["map"] = currentLine[11:-1]

        #all event baced stuff (the main bits)
        elif currentLine == "{":
            event = content[i - 1]
            # only gather data if warmup has ended
            if event == "round_announce_warmup":
                #warmup has ended
                rounds.clear()

            elif "round_end" == event:
                #round has ended so compile stats and prepare for next round
                roundWinner = int(content[i+1][9:10])
                if (roundWinner == 2 and not teamMultiplyer) or roundWinner == 3 and teamMultiplyer:
                    team1Score += 1
                    round["winner"] = 1
                else:
                    team2Score += 1
                    round["winner"] = 2

                round["team1Shots"] = team1Shots[:]
                round["team2Shots"] = team2Shots[:]

                round["team1Deaths"] = team1Deaths[:]
                round["team2Deaths"] = team2Deaths[:]

                round["team1Hits"] = team1Hits[:]
                round["team2Hits"] = team2Hits[:]

                rounds.append(round.copy())

                round.clear()

                team1Shots.clear()
                team2Shots.clear()

                team1Hits.clear()
                team2Hits.clear()

                team1Deaths.clear()
                team2Deaths.clear()

            elif event == "announce_phase_end":
                # Check if we are switching sides
                #Half change
                teamMultiplyer = not teamMultiplyer
                halfs.append(rounds[:])
                rounds.clear()

            elif event == "weapon_fire":
                #weapon has been fired (inc nades...)
                shot = {}
                shot["gun"] = content[i + 5][9:-1]
                tick = findCurrentTick(i, content)
                shot["time"] = (tick - tickOfRoundStart) * tickInterval

                if (content[i + 4][8:] == "CT" and teamMultiplyer) or (
                            (content[i + 4][8:] == "T") and not teamMultiplyer):
                    team1Shots.append(shot)
                else:
                    team2Shots.append(shot)
            elif event == "player_hurt":
                #player has been hurt
                shot = {}
                shot["PlayerHurt"] = content[i + 1][9:]
                shot["shotBy"] = content[i + 5][11:]
                shot["damage"] = content[i + 12][13:-1]
                shot["gun"] = content[i + 11][9:-1]
                shot["hitGroup"] = content[i + 14][11:-1]

                tick = findCurrentTick(i, content)
                if (tick - tickOfRoundStart) * tickInterval < 0:
                    print((tick - tickOfRoundStart) * tickInterval)
                    print(shot)
                    print()
                shot["time"] = (tick - tickOfRoundStart) * tickInterval

                if (content[i + 4][8:] == "CT" and teamMultiplyer) or (
                                content[i + 4][8:] == "T" and not teamMultiplyer):
                    team1Hits.append(shot)
                else:
                    team2Hits.append(shot)

            elif event == "player_death":
                #player has been killed
                kill = {}
                kill["Player"] = content[i + 1][9:]
                kill["killedBy"] = content[i + 5][11:]

                # if there was no assister then dont include it
                if not content[i + 9][11:] == "0 ":
                    kill["assistedBy"] = content[i + 9][11:]

                # if there was an assister then the remainign statistics will be 3 lines lower.
                offset = 0 if "weapon:" in content[i + 10] else 3

                kill["gun"] = content[i + 10 + offset][9:]
                kill["headShot"] = content[i + 14 + offset][11:]

                # find time of kill
                tick = findCurrentTick(i, content)
                if (tick - tickOfRoundStart) * tickInterval < 0:
                    print((tick - tickOfRoundStart) * tickInterval)
                    print(kill)
                    print()
                kill["time"] = (tick - tickOfRoundStart) * tickInterval

                if (content[i + 4][8:] == "CT" and teamMultiplyer) or (
                                content[i + 4][8:] == "T" and not teamMultiplyer):
                    team1Deaths.append(kill)
                else:
                    team2Deaths.append(kill)
            elif event == "round_freeze_end":
                # round has started (freze time ended)
                tickOfRoundStart = findCurrentTick(i, content)
            elif event == "player_footstep":
                #This is a hack becuase frezz time end dose not always happen
                if tickOfRoundStart == -1:
                    tickOfRoundStart = findCurrentTick(i, content)

    #we have now parsed the whole file so add a few extra fields to finish it off
    jsonData["tickRate"] = 1 / tickInterval
    if eventId != None:
        jsonData["event"] = eventId
    jsonData["team1Score"] = team1Score
    jsonData["team2Score"] = team2Score
    if len(rounds) != 0:
        halfs.append(rounds[:])
    jsonData["halfs"] = halfs
    # print(json.dumps(jsonData))
    # # save in mongoDB
    collection.insert_one(jsonData).inserted_id
    print("Demo parsed and saved to mongo")


# setup mongoDB connection
client = MongoClient()
collection = client.db.games

event = None

#for eatch file in demos folder parse it as though it is a demo, and for eatch folder in demos folder assume its name is the event id and parse each demo in it
count = -1
events = []
for root, dirs, files in os.walk("demos"):
    for file in files:
        if count == -1:
            parseDemo(file, None)
            gc.collect()#Force GC clean up to ensure we dont run out of memioury
        else:
            parseDemo(file, events[count])
            gc.collect()#Force GC clean up to ensure we dont run out of memioury
    for folder in dirs:
        events.append(folder)
    count += 1

#Close mongo connection
client.close()