import json
import time
import scraper

f = open('Inters.json')
data = json.load(f)

# Data stuff
def newPlayer(username):
    player = {
            "id": scraper.getid(username),
            "discordID": 0,
            "gameCount": 0,
            "kills": 0,
            "deaths": 0,
            "assists": 0
    }
    data[username] = player
    with open('Inters.json', "w") as f:
        json.dump(data, f, indent=4)


def updateStats(k,d,a, numGames, username):
    
    def updateDeaths(num):
        with open('Inters.json', "w") as f:
            data[username]["deaths"]+=num
            json.dump(data, f, indent=4)

    def updateKills(num):
        with open('Inters.json', "w") as f:
            data[username]["kills"]+=num
            json.dump(data, f, indent=4)

    def updateAssists(num):
        with open('Inters.json', "w") as f:
            data[username]["assists"]+=num
            json.dump(data, f, indent=4)

    def updateNumGame(num):
        with open('Inters.json', "w") as f:
            data[username]["gameCount"]=num
            json.dump(data, f, indent=4)
        
    updateKills(k)
    updateDeaths(d)
    updateAssists(a)
    updateNumGame(numGames)

def extractData(file):
    dataList = []
    with open(file) as f:
        for jsonObj in f:
            dataDict = json.loads(jsonObj)
            dataList.append(dataDict)
    return dataList

def checkChange(username):
    scraper.logData('HanooStreet', 1, 0)
    uid = getUID(username)
    dataList = extractData(f'{uid}.json')
    currGameCount = data[username]["gameCount"]
    final = dataList[len(dataList)-1]['deaths'][0]
    if (len(dataList) > currGameCount):
        for x in range(len(dataList)-currGameCount):
            kills = extractData(f'{uid}.json')[currGameCount+x]['kills'][0]
            deaths = extractData(f'{uid}.json')[currGameCount+x]['deaths'][0]
            assists = extractData(f'{uid}.json')[currGameCount+x]['assists']
            updateStats(kills, deaths, assists, len(dataList), username)
        return final
    else:
        print("All Data Recorded")
        return -1

def getUID(username):
    return data[username]['id']

def doesExist(username):
    try:
        print(data[username])
        return True
    finally:
        return False

def getDeaths(username):
    return data[username]['deaths']